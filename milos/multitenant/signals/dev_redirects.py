from ..models import ProxySite, DevDomainRedirect, SiteFolder
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

#http://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project/22924754#22924754

@receiver(post_save, sender=Site)
def create_dev_redirect(sender, instance, created, **kwargs):
	if created:
		dev = DevDomainRedirect.create_dev_domain(instance)