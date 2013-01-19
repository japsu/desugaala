from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^status$', 'status.views.status_page')
)