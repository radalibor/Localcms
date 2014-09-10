from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import viewsets, routers
from dashboard.urls import urlpatterns as dashboard_patterns
from sales.urls import urlpatterns as sales_patterns
from django.contrib import admin
admin.autodiscover()

from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import CreateView, ListView, DetailView

################################################3

#Router starts
from routers_factory import MasterRouter
from _base.viewsets import UserViewSet, GroupViewSet

router = MasterRouter("OUR_MODULES")

#_base
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)

################################################3

#from login.views import Login

urlpatterns = patterns('',
	url(r'^api/v1/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

	url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
	url(r'^admin/', include(admin.site.urls)),
	url(r'', include('dashboard.urls')),
	url(r'sales/', include('sales.urls', namespace='sales')),
	url(r'', include('tasks.urls')),
	#url(r'', include('messages.urls')),

	#url(r'products/', ProductListview.as_view(), name='product-list),
	url(r'contacts/', include('contact.urls.contact', namespace="contact")),
	url(r'organizations/', include('contact.urls.organization', namespace="organization")),
	url(r'products/', include('product.urls.product', namespace="product")),
	url(r'skus/', include('product.urls.sku', namespace="sku")),

	url(r'questionnaire/', include('questionnaire.urls', namespace='questionnaire')),

	url(r'^messages/', include('django_messages.urls')),
	url(r'^tasks/', include('project.urls', namespace='project')),
	url(r'^ticketing/', include('ticketing.urls', namespace="ticketing")),
	url(r'^pdf/', include('pdf.urls', namespace="pdf")),

	url(r'^accounts/', include('login.urls', namespace='login')),
	#LOGIN using alluth alternate:
	#alternate allauth which handles login (given override template Broadconnect -> TEMPLATES -> account -> login.html)
	url(r'^accounts/', include('allauth.urls')),

	#url(r'^accounts/profile/', RedirectView.as_view(url=reverse_lazy('ticketing:customer_ticket_list'))),
	url(r'^support/', include('support.urls', namespace="support")),
	url(r'^pre-sales/', include('pre_sales.urls', namespace="pre-sales")),
    url(r'^support/', include('support.urls', namespace="support")),
    url(r'^doc/', include('doc_confluence.urls', namespace="doc")),
	)

if settings.DEBUG:
	urlpatterns = patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
		url(r'', include('django.contrib.staticfiles.urls')),
		) + urlpatterns
