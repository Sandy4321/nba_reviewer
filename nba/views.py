from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from datetime import datetime, timedelta, time


from nba.models import Team, Game, GameComment, GameRating

class IndexView(generic.ListView):
    template_name = 'nba/game_list.html'
    context_object_name = 'game_list'

    def get_queryset(self, x=None):
        """Show only the games of today."""
        return Game().get_games()
        
        
class DetailView(generic.DetailView):
    model = Game
    template_name = 'nba/game_detail.html'


class CommentsView(generic.DetailView):
    model = Game
    template_name = 'nba/game_comments.html'


def review(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    try:
        comment_text = request.POST['review']
        comment_conclusion = request.POST['conclusion']

        rating_offence = request.POST['rating_offence']
        rating_defence = request.POST['rating_defence']
        rating_commentary = request.POST['rating_commentary']

        c = GameComment()
        c.text = comment_text
        c.conclusion = comment_conclusion
        c.game = game
        c.date = datetime.now()
        c.save()

        r = GameRating()
        r.game = game
        r.offence = rating_offence
        r.defence = rating_defence
        r.commentary = rating_commentary
        r.save()

    except (KeyError, Game.DoesNotExist):
        return render(request, 'nba/error.html', {
            'game': game,
            'error_message': "Something went wrong",
        })
    else:
        return HttpResponseRedirect(reverse('games:detail', args=(game.id,)))