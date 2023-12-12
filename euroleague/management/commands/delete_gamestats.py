from django.core.management.base import BaseCommand
from euroleague.models import GameStats  # Replace 'your_app' with the name of your app

class Command(BaseCommand):
    help = 'Deletes all GameStats records'

    def handle(self, *args, **options):
        GameStats.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all GameStats records'))
