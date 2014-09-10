from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site

from .models import *

#Unregister the normal sites admin
admin.site.unregister(Site)

class SubdomainInline(admin.TabularInline):
	model = Subdomain
	extra = 1

class SiteFolderInline(admin.TabularInline):
	model = SiteFolder
	extra = 1

class DevDomainRedirectInline(admin.TabularInline):
	model = DevDomainRedirect
	extra = 1

class DomainRedirectInline(admin.TabularInline):
	model = DomainRedirect
	extra = 1

class SiteAdmin(admin.ModelAdmin):
	inlines = [SubdomainInline, SiteFolderInline, DevDomainRedirectInline]

admin.site.register(Site, SiteAdmin)
admin.site.register(DomainRedirect)
admin.site.register(DevDomainRedirect)