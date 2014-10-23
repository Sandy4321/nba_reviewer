from django.db import models
from django.utils import timezone
import datetime

class Game(models.Model):

	# Columns
	home_id = models.CharField(max_length=16) 
	away_id = models.CharField(max_length=16)
	game_id = models.CharField(max_length=16)


class Team(models.Model):
	city = models.CharField(max_length=100)
	nickname = models.CharField(max_length=100)
	team_id = models.CharField(max_length=16)
	key = models.CharField(max_length=3)