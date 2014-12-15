from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime, timedelta, time


class Team(models.Model):

	team_id = models.CharField(unique=True, max_length=16)
	city = models.CharField(max_length=64)
	nickname = models.CharField(max_length=64)
	key = models.CharField(max_length=3)

	def __unicode__(self):
		return self.nickname


class Game(models.Model):

	game_id = models.CharField(unique=True, max_length=16)
	date = models.DateTimeField()
	home = models.ForeignKey('Team', to_field='team_id', related_name='game_home')
	away = models.ForeignKey('Team', to_field='team_id', related_name='game_away')
	home_score = models.IntegerField(null=True)
	away_score = models.IntegerField(null=True)

	def get_today_games(self):
		today = datetime.now().date()
		tomorrow = today + timedelta(1)
		today_start = datetime.combine(today, time())
		today_end = datetime.combine(tomorrow, time())

		return Game.objects.filter(date__lte=today_end, date__gte=today_start)

	def __unicode__(self):
		return '%s - %s (%s)' % (self.home, self.away, self.date)


class CommentCategory(models.Model):

	category_name = models.CharField(max_length=64)

	def __unicode__(self):
		return self.category_name


class Comment(models.Model):
	
	comment_category = models.ForeignKey(CommentCategory, blank=True, null=True)
	game = models.ForeignKey(Game)
	rating = models.IntegerField(default=0)
	text = models.CharField(max_length=1024)
	date = models.DateTimeField()

	def __unicode__(self):
		return self.text