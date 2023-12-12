from django.db.models.signals import post_save  
from django.contrib.auth.models import User    
from django.dispatch import receiver            
from .models import Profilis

# When a user is created, a profile is automatically created.
@receiver(post_save, sender=User) # If a User object is saved, this function is initiated after the decorator.
def create_profile(sender, instance, created, **kwargs): # 'instance' represents the newly created User object.
    if created:
        Profilis.objects.create(user=instance)
        print('KWARGS: ', kwargs)


# When a user is modified, the profile is saved.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profilis'):
        instance.profilis.save()


