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


class ResultsView(generic.DetailView):
    model = Game
    template_name = 'nba/nba_results.html'

def vote(request, poll_id):
    p = get_object_or_404(Game, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))