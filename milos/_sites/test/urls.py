from django.conf.urls import patterns, include, url

from django.contrib.flatpages import views
from django.contrib.sites.models import Site



urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    
)
