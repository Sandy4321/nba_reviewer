from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.dates import DayArchiveView
from datetime import datetime, timedelta, time
from pytz import timezone
from nba.models import Team, Game, GameComment, GameRating
from nba.forms import UserForm, UserProfileForm
from django.template import RequestContext, loader


def profile(request):
    template = loader.get_template('profile/profile.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('about/about.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def contact(request):
    template = loader.get_template('contact/contact.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))