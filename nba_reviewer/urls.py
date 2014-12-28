from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nba_reviewer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^games/', include('nba.urls', namespace="games")),
    url(r'^admin/', include(admin.site.urls)),
)
