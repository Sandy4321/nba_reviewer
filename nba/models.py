from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime, timedelta, time
from pytz import timezone


class Team(models.Model):

	team_id = models.CharField(unique=True, max_length=16)
	city = models.CharField(max_length=64)
	nickname = models.CharField(max_length=64)
	key = models.CharField(max_length=3)

	def __unicode__(self):
		return self.nickname


class Game(models.Model):

	game_id = models.CharField(unique=True, max_length=16)
	date = models.DateTimeField(null=True)
	home = models.ForeignKey('Team', to_field='team_id', related_name='game_home')
	away = models.ForeignKey('Team', to_field='team_id', related_name='game_away')
	home_score = models.IntegerField(null=True)
	away_score = models.IntegerField(null=True)

	def get_games(self):
		today = datetime.now(timezone('EST'))
		tomorrow = today + timedelta(1)
		today_start = datetime.combine(today, time())
		today_end = datetime.combine(tomorrow, time())

		return Game.objects.filter(date__lte=today_end, date__gte=today_start).order_by('date')


	def rating(self):
		gameratings = GameRating.objects.filter(game = self)

		total_offence = 0
		total_defence = 0
		total_commentary = 0
		length = float(len(gameratings))

		for game in gameratings:
			total_offence += game.offence
			total_defence += game.defence
			total_commentary += game.commentary

		return {'offence' : int((total_offence / length) * 10), 'defence' : int((total_defence / length) * 10), 'commentary' : int((total_commentary / length) * 10)}

	def __unicode__(self):
		return '%s - %s (%s)' % (self.home, self.away, self.date)


class GameRating(models.Model):
	game = models.ForeignKey(Game)
	offence = models.IntegerField(default=0)
	defence = models.IntegerField(default=0)
	commentary = models.IntegerField(default=0)

	def sum(self):
		gameratings = GameRating.objects.filter(game = self.game)

		total_offence = 0
		total_defence = 0
		total_commentary = 0
		length = len(gameratings)

		for game in gameratings:
			total_offence += game.offence
			total_defence += game.defence
			total_commentary += game.commentary

		return {'offence' : total_offence / length, 'defence' : total_defence / length, 'commentary' : total_commentary / length}


class GameComment(models.Model):
	game = models.ForeignKey(Game)
	text = models.CharField(max_length=1024)
	conclusion = models.CharField(max_length=128)
	date = models.DateTimeField()
	
	def __unicode__(self):
		return self.conclusion