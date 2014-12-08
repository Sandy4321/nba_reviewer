from django.contrib import admin
from nba.models import Game, Team

# Register your models here.

class GameAdmin(admin.ModelAdmin):
	fieldsets = [
        ('Team Home',          {'fields': ['home']}),
    ]

admin.site.register(Game, GameAdmin)
