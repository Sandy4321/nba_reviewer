from django.conf.urls import patterns, url
from nba import views

urlpatterns = patterns('',
	url(r'^$', views.HomePageRedirect, name='index'),
    url(r'^(?P<pk>\d+)/detail/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/comments/$', views.CommentsView.as_view(), name='comments'),
    url(r'^(?P<game_id>\d+)/review/$', views.review, name='review'),
    url(r'^(?P<game_id>\d+)(?P<user_id>\d+)/$', views.setwatched, name='setwatched'),
    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<day>\d+)/$', views.GameDayArchiveView.as_view(), name="game_day"),
)