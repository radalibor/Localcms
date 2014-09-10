from django.conf import settings
from django.contrib.sites.models import Site

import os

def current_site(request):
	return (settings.SITE_ID) and {
	'site': Site.objects.get_current(),
	'BOWER_URL': os.path.join(settings.STATIC_URL, Site.objects.get_current().folder_name.path, 'bower_components') + '/',
	'SITE_STATIC': os.path.join(settings.STATIC_URL, Site.objects.get_current().folder_name.path) + '/',
	} or {}