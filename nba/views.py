from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.dates import DayArchiveView
from datetime import datetime, timedelta, time
from pytz import timezone
from nba.models import Team, Game, GameComment, GameRating, GamePerUser
from django.contrib.auth.models import User
from nba.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


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


@login_required
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


@login_required
def setwatched(request, game_id, user_id):
    try:
        game_per_user = GamePerUser.objects.filter(game_id=game_id,user_id=user_id)

        if not game_per_user:
            try:
                gpu = GamePerUser()
                gpu.game = Game(id=game_id)
                gpu.user = User(id=user_id)
                gpu.watched = True
                gpu.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
           

        else:
            game_per_user = game_per_user[0]

            if game_per_user.watched == True:
                game_per_user.watched = False
            else:
                game_per_user.watched = True

            game_per_user.save()

    except:
        return render(request, 'nba/error.html', {
            'error_message': "Something went wrong",
        })
    else:
        return HttpResponseRedirect(reverse('games:detail', args=(game_id,)))


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration
    # succeeds.
    registered = False
    registration_error = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was
            # successful.
            registered = True
            registration_error = False

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
            registration_error = True

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
        'registration/register.html',
        {'user_form': user_form, 'registered': registered,
            'registration_error': registration_error},
        context)
