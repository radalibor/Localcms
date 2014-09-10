from ..models import SiteFolder
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

#http://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project/22924754#22924754

@receiver(post_save, sender=Site)
def create_sitefolder(sender, instance, created, **kwargs):
	if created:
		sf = SiteFolder.create(instance)

@receiver(post_save, sender=SiteFolder)
def create_sitefolder_path(sender, instance, created, **kwargs):
	if created:
		path = SiteFolder.create_path(instance)

@receiver(post_save, sender=SiteFolder)
def create_static_folders(sender, instance, created, **kwargs):
	if created:
		SiteFolder.create_static_folders(instance)