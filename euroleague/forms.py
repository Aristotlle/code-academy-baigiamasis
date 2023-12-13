from .models import Team

from django import forms
from django.contrib.auth.models import User

# Form for updating user information.
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Form for making match predictions.
class PredictionForm(forms.Form):
    team = forms.ChoiceField(label='Select Team')
    opponent = forms.ChoiceField(label='Select Opponent')

    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)
        team_choices = [(team.id, team.name) for team in Team.objects.all()]
        self.fields['team'].choices = team_choices
        self.fields['opponent'].choices = team_choices