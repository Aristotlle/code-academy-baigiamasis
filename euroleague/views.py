from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import HttpResponse
from .models import Team, City, League, GameStats, EuroLeagueFact
from django.views import generic
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.db.models import Case, When, FloatField, Avg, Q, Func, F
from django.contrib.auth.decorators import login_required
from .forms import  UserUpdateForm, ProfilisUpdateForm, PredictionForm
import pickle
import os
from django.conf import settings
import pandas as pd
from .utils import rf_model, load_averages_data
import random

# Define a custom SQL function for rounding numbers
class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'
    
# Define the index view
def index(request):
    num_teams = Team.objects.all().count()
    num_leagues = League.objects.count()
    num_cities = City.objects.count()
    teams = Team.objects.all()

   # Fetching a random EuroLeague fact
    all_facts = EuroLeagueFact.objects.all()
    if all_facts:
        random_fact = random.choice(all_facts).fact_text
    else:
        random_fact = 'No facts available at the moment.'
    
     # Tracking the number of visits
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Updating the context dictionary to include the random fact
    context = {
        'num_teams': num_teams,
        'num_leagues': num_leagues,
        'num_cities': num_cities,
        'num_visits': num_visits,
        'team_list': teams,
        'random_fact': random_fact,  
    }

    return render(request, 'index.html', context=context)

# Define a class-based view for listing teams
class TeamListView(generic.ListView):
    model = Team
    paginate_by = 18
    template_name = 'team_list.html'

# Define a class-based view for displaying team details
class TeamDetailView(generic.DetailView):
    model = Team
    template_name = 'team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object
        teams = Team.objects.all()
        wins = GameStats.objects.filter(team=team, win_loss='W').count()
        losses = GameStats.objects.filter(team=team, win_loss='L').count()
        
         # Calculate averages for the team for both home and away games
        stats = GameStats.objects.filter(
            Q(team=team) | Q(opponent_team=team)
        ).annotate(
            points=Case(
                When(team=team, then='points_home'),
                When(opponent_team=team, then='points_away'),
                default=0,
                output_field=FloatField()
            ),
            rebounds=Case(
                When(team=team, then='total_rebounds_home'),
                When(opponent_team=team, then='total_rebounds_away'),
                default=0,
                output_field=FloatField()
            ),
            steals=Case(
                When(team=team, then='steals_home'),
                When(opponent_team=team, then='steals_away'),
                default=0,
                output_field=FloatField()
            ),
            blocks=Case(
                When(team=team, then='blocks_home'),
                When(opponent_team=team, then='blocks_away'),
                default=0,
                output_field=FloatField()
            ),
            pir=Case(
                When(team=team, then='pir_home'),
                When(opponent_team=team, then='pir_away'),
                default=0,
                output_field=FloatField()
            ),
            assists=Case(
                When(team=team, then='assists_home'),
                When(opponent_team=team, then='assists_away'),
                default=0,
                output_field=FloatField()
            ),
        ).order_by('round_number') 
        
        

        averages = stats.aggregate(
            average_PTS=Round(Avg('points')),
            average_TR=Round(Avg('rebounds')),
            average_ST=Round(Avg('steals')),
            average_BLK=Round(Avg('blocks')),
            average_PIR=Round(Avg('pir')),
            average_AST=Round(Avg('assists'))
            # Aggregations for other annotated fields...
        )

        game_stats = GameStats.objects.filter(Q(team=team) | Q(opponent_team=team)).order_by('round_number')
   # Update the context with the calculated averages
        context.update({
            'average_PTS': averages.get('average_PTS'),
            'average_TR' : averages.get('average_TR'),
            'average_ST' : averages.get('average_ST'),
            'average_BLK' : averages.get('average_BLK'),
            'average_PIR': averages.get("average_PIR"),
            'average_AST': averages.get('average_AST'),
            'game_stats': game_stats,
            'team_list': teams,
            'wins':wins,
            'losses': losses
            # Updates for other averages...
            
        })
        
        return context
    
# Define a function to map team ID to code    
def map_team_id_to_code(team_id):
    try:
        return Team.objects.get(id=team_id).tm_code
    except Team.DoesNotExist:
        return None  

# Define a view for predictions
def predict_view(request):
    team_list = Team.objects.all()
    form = PredictionForm()

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            team_id = form.cleaned_data['team']
            opponent_id = form.cleaned_data['opponent']

            try:
                team = Team.objects.get(id=team_id)
                opponent = Team.objects.get(id=opponent_id)
                team_code = team.tm_code
                opponent_code = opponent.tm_code
            except Team.DoesNotExist:
                # Handle the case where the team does not exist
                return render(request, 'error.html', {'message': 'Team not found'})

            averages_df = load_averages_data()

            # Extracting statistics for the selected teams
            team_stats = averages_df[averages_df['tm_code'] == team_code]
            opponent_stats = averages_df[averages_df['tm_code'] == opponent_code]

            # Preparing input data
            input_data = [
                [
                    team_code,
                    opponent_code,
                    team_stats['Average PTS'].iloc[0],
                    opponent_stats['Average PTS'].iloc[0],
                    team_stats['Average 2PTM'].iloc[0],
                    opponent_stats['Average 2PTM'].iloc[0],
                    team_stats['Average AST'].iloc[0],
                    opponent_stats['Average AST'].iloc[0],
                    team_stats['Average ST'].iloc[0],
                    opponent_stats['Average ST'].iloc[0],
                    team_stats['Average BLK'].iloc[0],
                    opponent_stats['Average BLK'].iloc[0],
                    team_stats['Average TR'].iloc[0],
                    opponent_stats['Average TR'].iloc[0],
                    team_stats['Average PIR'].iloc[0],
                    opponent_stats['Average PIR'].iloc[0],
                ]
            ]
            columns = ['tm_code','opp_code','PTS_home','PTS_away','2PTM_home','2PTM_away','AST_home','AST_away','ST_home','ST_away','BLK_home','BLK_away','TR_home','TR_away','PIR_home','PIR_away']
            input_df = pd.DataFrame(input_data, columns=columns)

            # Make a prediction using the loaded model
            predicted_outcome = rf_model.predict(input_df)
            result = "Win" if predicted_outcome[0] == 1 else "Lose"
            
            # Process and compare the stats
            
            processed_team_stats = {
                'AveragePTS': team_stats['Average PTS'].iloc[0],
                'Average2PTM': team_stats['Average 2PTM'].iloc[0],
                'AverageAST': team_stats['Average AST'].iloc[0],
                'AverageST': team_stats['Average ST'].iloc[0],
                'AverageBLK': team_stats['Average BLK'].iloc[0],
                'AverageTR': team_stats['Average TR'].iloc[0],
                'AveragePIR': team_stats['Average PIR'].iloc[0],
            }
            processed_opponent_stats = {
                'AveragePTS': opponent_stats['Average PTS'].iloc[0],
                'Average2PTM': opponent_stats['Average 2PTM'].iloc[0],
                'AverageAST': opponent_stats['Average AST'].iloc[0],
                'AverageST': opponent_stats['Average ST'].iloc[0],
                'AverageBLK': opponent_stats['Average BLK'].iloc[0],
                'AverageTR': opponent_stats['Average TR'].iloc[0],
                'AveragePIR': opponent_stats['Average PIR'].iloc[0],
            }


            # Storing processed data in session
            request.session['team_averages'] = processed_team_stats
            request.session['opponent_averages'] = processed_opponent_stats

            # Storing prediction results in session
            request.session['team_name'] = team.name
            request.session['opponent_name'] = opponent.name
            request.session['outcome'] = "Win" if predicted_outcome[0] == 1 else "Lose"

            # Redirect to the result page
            return redirect('prediction_result')

    # Render the prediction form page in case of GET request or form invalidation
    return render(request, 'predict.html', {'form': form, 'team_list':team_list})


def prediction_result_view(request):
    # Extract the result and averages from the session
    context = {
        'team_name': request.session.get('team_name'),
        'opponent_name': request.session.get('opponent_name'),
        'result': request.session.get('outcome', 'No result available'),
        'team_averages': request.session.get('team_averages', {}),
        'opponent_averages': request.session.get('opponent_averages', {}),
        'team_list': Team.objects.all(),
    }

    # Clear the session after retrieving the data
    for key in ['team_name', 'opponent_name', 'outcome', 'team_averages', 'opponent_averages']:
        request.session.pop(key, None)

    # Render the result page
    return render(request, 'prediction_result.html', context)



@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


def search(request):
    query = request.GET.get('query')
    search_results = Team.objects.filter(Q(name__icontains=query) | Q(summary__icontains=query))
    team_list = Team.objects.all()  # Query to get all teams
    return render(request, 'search.html', {'teams': search_results, 'query': query, 'team_list': team_list})




@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)