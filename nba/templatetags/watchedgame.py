from django import template
from nba.models import GamePerUser

register = template.Library()


def watched(game, user):
    game_per_user = GamePerUser.objects.filter(game_id=game.id,user_id=user.id)
    if game_per_user:
    	return game_per_user[0].watched
    return False
    	

register.filter('watched', watched)
