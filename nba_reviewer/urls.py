from django.conf.urls import patterns, include, url
import nba
import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^games/', include('nba.urls', namespace="games")),
    url(r'^about/', views.about),
    url(r'^contact/', views.contact),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': '/games'}),
    url(r'^register/$', nba.views.register, name='register'),
)
