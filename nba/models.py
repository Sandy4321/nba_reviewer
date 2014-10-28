from django.db import models
from django.utils import timezone
import datetime


class Team(models.Model):

	team_id = models.CharField(unique=True, max_length=16)
	city = models.CharField(max_length=64)
	nickname = models.CharField(max_length=64)
	key = models.CharField(max_length=3)


class Game(models.Model):

	game_id = models.CharField(unique=True, max_length=16)
	date = models.DateTimeField()
	home = models.ForeignKey('Team', to_field='team_id', related_name='game_home')
	away = models.ForeignKey('Team', to_field='team_id', related_name='game_away')
	home_score = models.IntegerField(null=True)
	away_score = models.IntegerField(null=True)	


