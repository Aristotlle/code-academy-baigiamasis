from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from euroleague.models import Team, GameStats  # Adjust the import path according to your app's structure

class Command(BaseCommand):
    help = 'Populates the GameStats model from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        try:
             # Read the data from the specified CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path)
            # Loop through each row of the DataFrame and create GameStats objects  
            for _, row in df.iterrows():
                team = Team.objects.get(tm_code=row['tm_code'])
                opponent_team = Team.objects.get(tm_code=row['opp_code'])

                GameStats.objects.create(
                    round_number=row['ROUND'],
                    team=team,
                    opponent_team=opponent_team,
                    win_loss='W' if row['W/L'] == 1 else 'L',
                    points_home=row['PTS_home'],
                    points_away=row['PTS_away'],
                    field_goals_made_home=row['2PTM_home'],
                    field_goals_made_away=row['2PTM_away'],
                    assists_home=row['AST_home'],
                    assists_away=row['AST_away'],
                    steals_home=row['ST_home'],
                    steals_away=row['ST_away'],
                    blocks_home=row['BLK_home'],
                    blocks_away=row['BLK_away'],
                    total_rebounds_home=row['TR_home'],
                    total_rebounds_away=row['TR_away'],
                    pir_home=row['PIR_home'],
                    pir_away=row['PIR_away']
                )

            self.stdout.write(self.style.SUCCESS('Successfully populated GameStats'))
        except Exception as e:
            raise CommandError(f'Error occurred: {e}')
