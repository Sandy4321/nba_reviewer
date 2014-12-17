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
        #selected_choice = p.choice_set.get(pk=request.POST['choice'])
        review_offence = request.POST['review_offence']
        review_defence = request.POST['review_defence']
        review_commentary = request.POST['review_commentary']

        rating_offence = request.POST['rating_offence']
        rating_defence = request.POST['rating_defence']
        rating_commentary = request.POST['rating_commentary']

        reviews = [ 
            { 'comment' : review_offence, 'rating': rating_offence, 'category' : CommentCategory.objects.get(category_name='Offence')}, 
            { 'comment' : review_defence , 'rating': rating_defence, 'category' : CommentCategory.objects.get(category_name='Defence') },
            { 'comment' : review_commentary, 'rating': rating_commentary, 'category' : CommentCategory.objects.get(category_name='Commentary')}
        ]

        for review in reviews:
            c = Comment()
            c.text = review.get('comment')
            c.rating = (int(review.get('rating')) * 10)
            c.game = game
            c.date = datetime.now()
            c.comment_category = review.get('category')
            c.save()

    except (KeyError, Game.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'games/detail.html', {
            'game': game,
            'error_message': "Something went wrong",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('games:detail', args=(game.id,)))