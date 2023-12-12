from django.apps import AppConfig


  # Setting the default field type for primary keys in your models
class EuroleagueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'euroleague'
    
    # The ready method is overridden to perform initialization tasks such as 
    # registering signals. This is called as soon as the app registry is fully populated.
    def ready(self):
        # Importing signal handlers. This is done inside the ready method to ensure 
        # that all app models are loaded before importing the signal handlers 
        # to avoid issues with circular imports.
        from .signals import create_profile, save_profile
