from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime, timedelta, time
from pytz import timezone
from django.contrib.auth.models import User


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
    home = models.ForeignKey(
        'Team', to_field='team_id', related_name='game_home')
    away = models.ForeignKey(
        'Team', to_field='team_id', related_name='game_away')
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)

    def rating(self):
        gameratings = GameRating.objects.filter(game=self)

        total_offence = 0
        total_defence = 0
        total_commentary = 0
        length = float(len(gameratings))

        if length == 0:
            return

        for game in gameratings:
            total_offence += game.offence
            total_defence += game.defence
            total_commentary += game.commentary

        total_offence = int((total_offence / length) * 10)
        total_defence = int((total_defence / length) * 10)
        total_commentary = int((total_commentary / length) * 10)

        total = int((total_offence + total_defence + total_commentary) / 3)

        return {
            'offence': total_offence,
            'defence': total_defence,
            'commentary': total_commentary,
            'total': total
        }

    def __unicode__(self):
        return '%s - %s (%s)' % (self.home, self.away, self.date)


class GamePerUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    watched = models.BooleanField()


class GameRating(models.Model):
    game = models.ForeignKey(Game)
    offence = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    commentary = models.IntegerField(default=0)


class GameComment(models.Model):
    game = models.ForeignKey(Game)
    text = models.CharField(max_length=1024)
    conclusion = models.CharField(max_length=128)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.conclusion
