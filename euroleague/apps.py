from django.apps import AppConfig


class EuroleagueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'euroleague'
    
    def ready(self):
        from .signals import create_profile, save_profile