from django.apps import AppConfig


  # Setting the default field type for primary keys in your models
class EuroleagueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'euroleague'
    
