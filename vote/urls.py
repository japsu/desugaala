from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'vote.views.vote_page')
)