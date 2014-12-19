from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from datetime import datetime, timedelta, time


from nba.models import Team, Game, Comment, CommentCategory

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


def review(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    try:
        comment_text = request.POST['review']

        rating_offence = request.POST['rating_offence']
        rating_defence = request.POST['rating_defence']
        rating_commentary = request.POST['rating_commentary']

        reviews = [ 
            {'rating': rating_offence, 'category' : CommentCategory.objects.get(category_name='Offence')}, 
            {'rating': rating_defence, 'category' : CommentCategory.objects.get(category_name='Defence') },
            {'rating': rating_commentary, 'category' : CommentCategory.objects.get(category_name='Commentary')}
        ]

        for review in reviews:
            c = Comment.objects.filter(comment_category=review.get('category'), game=game)

            if c:
                c = c[0]
                comment_rating = c.rating
                c.rating = comment_rating + (int(review.get('rating')) * 10)
                c.amount += 1
                c.game = game
                c.comment_category = review.get('category')
                c.date = datetime.now()
                c.save()
            else:
                c = Comment()
                c.amount = 1
                c.rating = (int(review.get('rating')) * 10)
                c.game = game
                c.comment_category = review.get('category')
                c.date = datetime.now()
                c.save()

        c = Comment()
        c.text = comment_text
        c.game = game
        c.date = datetime.now()
        c.save()

    except (KeyError, Game.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'nba/error.html', {
            'game': game,
            'error_message': "Something went wrong",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('games:detail', args=(game.id,)))