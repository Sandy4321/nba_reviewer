from django.conf.urls import patterns, url
from nba import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/detail/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/comments/$', views.CommentsView.as_view(), name='comments'),
    url(r'^(?P<game_id>\d+)/review/$', views.review, name='review'),
)