from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from datetime import datetime, timedelta, time


from nba.models import Team, Game

class IndexView(generic.ListView):
    template_name = 'nba/game_list.html'
    context_object_name = 'today_games_list'

    def get_queryset(self):
        """Show only the games of today."""
        return Game().get_today_games()
        

class DetailView(generic.DetailView):
    model = Game
    template_name = 'nba/game_detail.html'


class CommentsView(generic.DetailView):
    model = Game
    template_name = 'nba/game_comments.html'