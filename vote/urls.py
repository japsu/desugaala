from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'vote.views.vote_page'),
    url(r'^login$', 'vote.views.login_api'),
    url(r'^vote$', 'vote.views.vote_api'),
)