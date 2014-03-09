from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'glass/oauth/authorize', 'python_glass.views.oauth_authorize'),
    url(r'glass/oauth/callback', 'python_glass.views.oauth_callback'),
)
