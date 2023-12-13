from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from PIL import Image

# Model for Fun Facts about EuroLeague
class EuroLeagueFact(models.Model):
    fact_text = models.TextField() # Text content of the fun fact
    date_added = models.DateTimeField(auto_now_add=True)# Date when the fact was added
    fact_category = models.CharField(max_length=100, blank=True)# Category for the fact (optional)

    def __str__(self):
        """String representation of the EuroLeagueFact."""
        return self.fact_text[:50] + '...' if len(self.fact_text) > 50 else self.fact_text # Short representation of the fact
    
    class Meta:
        verbose_name = "Fun facts"
        verbose_name_plural = 'Fun facts'


class City(models.Model):
    name = models.CharField(max_length=200, help_text='City name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = 'City'


class League(models.Model):
    name = models.CharField(max_length=200, help_text='League name')
    description = models.TextField(max_length=1000, blank=True, help_text='League description')

    def __str__(self):
        return self.name


        
        
class Team(models.Model):
    name = models.CharField(max_length=200, help_text='Team name')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='teams')
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, related_name='teams')
    summary = models.TextField(max_length=3000, help_text='Team summary')
    logo = models.ImageField(upload_to='team_logos', null=True, blank=True)
    tm_code = models.IntegerField(help_text='Team Code used for predictions', null=True)
   
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = 'Team'



class GameStats(models.Model):
    round_number = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team_stats', default=1)
    opponent_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team_stats',default=2)
    win_loss = models.CharField(max_length=1, default='W')  # "W" for win, "L" for loss
    points_home = models.IntegerField(default=0)
    points_away = models.IntegerField(default=0)
    field_goals_made_home = models.IntegerField(default=0)
    field_goals_made_away = models.IntegerField(default=0)
    assists_home = models.IntegerField(default=0)
    assists_away = models.IntegerField(default=0)
    steals_home = models.IntegerField(default=0)
    steals_away = models.IntegerField(default=0)
    blocks_home = models.IntegerField(default=0)
    blocks_away = models.IntegerField(default=0)
    total_rebounds_home = models.IntegerField(default=0)
    total_rebounds_away = models.IntegerField(default=0)
    pir_home = models.FloatField(default=0)
    pir_away = models.FloatField(default=0)
    tm_code = models.IntegerField(default=0)
    opp_code = models.IntegerField(default=0)

    def __str__(self):
        return (f"Round {self.round_number}: {self.team.name} vs {self.opponent_team.name} - "
                f"{'Win' if self.win_loss == 'W' else 'Loss'}")
        
    class Meta:
        verbose_name = "Game stats"
        verbose_name_plural = 'Game stats'


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = 'Profile'