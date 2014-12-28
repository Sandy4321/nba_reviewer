from django.shortcuts import get_object_or_404, render
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.dates import DayArchiveView
from datetime import datetime, timedelta, time
from pytz import timezone
from nba.models import Team, Game, GameComment, GameRating


def HomePageRedirect(request):
    current_day = datetime.now(timezone('EST'))
    year = current_day.strftime("%Y")
    month = current_day.strftime("%b")
    day = current_day.strftime("%d")

    return HttpResponseRedirect(reverse('games:game_day', args=(year, month, day)))


class GameDayArchiveView(DayArchiveView):
    queryset = Game.objects.all()
    date_field = "date"
    make_object_list = True
    allow_future = True


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
