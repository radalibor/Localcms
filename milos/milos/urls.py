from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import views
from django.contrib.sites.models import Site

admin.autodiscover()


urlpatterns = [
    # Examples:
    url(r'^$', 'milos.views.home', name='home'),
    url(r'^test/', include('test.urls')),
	url(r'^admin/', include(admin.site.urls)),
]
