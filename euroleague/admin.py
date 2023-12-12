from django.contrib import admin
from django.contrib import admin
from .models import City, League, Team,  Profilis, GameStats, EuroLeagueFact

# City Admin
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', )

# League Admin
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')



# Team Admin
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'league','tm_code')
    list_filter = ('city', 'league','tm_code')
    search_fields = ('name', 'city__name', 'league__name')

class StatsAdmin(admin.ModelAdmin):
    list_display = (
        'round_number', 'team', 'opponent_team', 'win_loss_display', 
        'points_home_display', 'points_away_display', 'field_goals_made_home_display', 
        'field_goals_made_away_display', 'assists_home_display', 'assists_away_display', 
        'steals_home_display', 'steals_away_display', 'blocks_home_display', 
        'blocks_away_display', 'total_rebounds_home_display', 'total_rebounds_away_display', 
        'pir_home_display', 'pir_away_display'
    )
    search_fields = (
        'round_number', 'team__name', 'opponent_team__name', 'win_loss',
        'points_home', 'points_away', 'field_goals_made_home',
        'field_goals_made_away', 'assists_home', 'assists_away',
        'steals_home', 'steals_away', 'blocks_home', 'blocks_away',
        'total_rebounds_home', 'total_rebounds_away', 'pir_home', 'pir_away'
    )

    def win_loss_display(self, obj):
        return obj.win_loss
    win_loss_display.short_description = 'W/L'

    def points_home_display(self, obj):
        return obj.points_home
    points_home_display.short_description = 'PTS H'

    def points_away_display(self, obj):
        return obj.points_away
    points_away_display.short_description = 'PTS A'

    def field_goals_made_home_display(self, obj):
        return obj.field_goals_made_home
    field_goals_made_home_display.short_description = 'FGM H'

    def field_goals_made_away_display(self, obj):
        return obj.field_goals_made_away
    field_goals_made_away_display.short_description = 'FGM A'
    
    def assists_home_display(self, obj):
        return obj.assists_home
    assists_home_display.short_description = 'AST H'

    def assists_away_display(self, obj):
        return obj.assists_away
    assists_away_display.short_description = 'AST A'

    def steals_home_display(self, obj):
        return obj.steals_home
    steals_home_display.short_description = 'ST H'

    def steals_away_display(self, obj):
        return obj.steals_away
    steals_away_display.short_description = 'ST A'

    def blocks_home_display(self, obj):
        return obj.blocks_home
    blocks_home_display.short_description = 'BLK H'

    def blocks_away_display(self, obj):
        return obj.blocks_away
    blocks_away_display.short_description = 'BLK A'

    def total_rebounds_home_display(self, obj):
        return obj.total_rebounds_home
    total_rebounds_home_display.short_description = 'TR H'

    def total_rebounds_away_display(self, obj):
        return obj.total_rebounds_away
    total_rebounds_away_display.short_description = 'TR A'

    def pir_home_display(self, obj):
        return obj.pir_home
    pir_home_display.short_description = 'PIR H'

    def pir_away_display(self, obj):
        return obj.pir_away
    pir_away_display.short_description = 'PIR A'
    

class EuroLeagueFactAdmin(admin.ModelAdmin):
    list_display = ('fact_text', 'date_added', 'fact_category')
    list_filter = ('date_added', 'fact_category')
    search_fields = ('fact_text',)


# Registering models to admin site
admin.site.register(City, CityAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(GameStats, StatsAdmin)
admin.site.register(Profilis)  
admin.site.register(EuroLeagueFact, EuroLeagueFactAdmin)
