from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

import os

'''
Inspired by
https://bitbucket.org/uysrc/django-dynamicsites/src/6c1ecec52a9c555ef3b7239171f9287a746330d3/dynamicsites/models.py?at=default
'''

class ProxySite(Site):
    class Meta:
        proxy = True

    @property
    def has_subdomains(self):
        return self.subdomains.exists()

    @property
    def subdomain_list(self):
        return self.subdomains.values_list('name', flat=True)


class SiteFolder(models.Model):
    site = models.OneToOneField('sites.Site', related_name='folder_name')
    path = models.CharField(max_length=255, help_text='name of folder for urls conf inside sites custom sites app')

    class Meta:
        verbose_name = _('Site Folder')
        verbose_name_plural = _('Site Folders')

    def __unicode__(self):
        return self.path

    @classmethod
    def create(cls, SiteInstance):        
        sf, created = SiteFolder.objects.get_or_create(
            site=SiteInstance,
            path=slugify(SiteInstance.name.split('.')[0])
            )
        if created:
            print 'SiteFolder object created: %s' % (sf.path)
        else:
            print 'SiteFolder object: %s - already exists!' % sf.path

        return sf

    @classmethod
    def create_path(cls, instance):
        sites_dir = settings.SITES_DIR
        folder_root = os.path.join(sites_dir, instance.path)

        if not os.path.exists(folder_root):
            os.mkdir(folder_root)
            if os.path.exists(folder_root):
                print '\tMade site folder path: %s' % folder_root

                # create an empty __init__.py file so this is a proper module

                # first, change the current directory
                os.chdir(folder_root)

                # write an empty file
                with open('__init__.py', 'wb') as init:
                    init.write('')

            else:
                print '\tUnable to make site folder path: %s' % folder_root

            templates_dir = os.path.join(folder_root, 'templates')
            if not os.path.exists(templates_dir):
                os.mkdir(templates_dir)
                if os.path.exists(templates_dir):
                    print '\tMade templates dir: %s' % templates_dir
                else:
                    print '\tUnable to make templates dir: %s' % templates_dir

        return folder_root

    @classmethod
    def create_static_folders(cls, instance):
        bower = settings.BOWER_DIR
        src = settings.SRC_DIR
        project = os.path.join(src, instance.path)
        project_bower = os.path.join(bower, instance.path)
        base = [bower, src, project, project_bower]

        for folder in base:
            if not os.path.exists(folder):
                os.mkdir(folder)
                print '\t--> Created directory at: %s' % folder

        less = os.path.join(project, 'less')
        css = os.path.join(project, 'css')
        js = os.path.join(project, 'js')
        img = os.path.join(project, 'img')
        fonts = os.path.join(project, 'fonts')

        allfolders = [less, css, js, img, fonts]
        for foobar in allfolders:
            if not os.path.exists(foobar):
                os.mkdir(foobar)
                print '\t--> Created: %s' % foobar

class Subdomain(models.Model):
    '''
    Unlike the 'dynamicsites' library, we are doing a proper foreign-key
    from the Subdomain to the Sites model.

    Also, we are not asking the user to specify a folder name, but instead,
    will get the folder name based on the exact name of the site, thereby
    ensuring that there is a one-to-one correlation.
    '''

    priority = models.IntegerField()
    site = models.ForeignKey('sites.Site', related_name='subdomains')
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Subdomain')
        verbose_name_plural = _('Subdomains')
        unique_together = ('priority', 'site',)

    def __full__(self):
        return '%s --> %s' % (self.name, self.site.domain)

    def __unicode__(self):
        return self.__full__()

class DomainRedirect(models.Model):
    site = models.ForeignKey('sites.Site', related_name='redirects')
    alternate = models.CharField(max_length=255, help_text='Just the domain part, not the full url.')

    class Meta:
        verbose_name = _('Domain Redirect')
        verbose_name_plural = _('Domain Redirects')

    def __full__(self):
        return '%s --> %s' % (self.alternate, self.site.domain)

    def __unicode__(self):
        return self.__full__()

    @classmethod
    def mapping_dict(cls):
        return {d.alternate:d.site.domain for d in cls.objects.all()}

class SubdomainRedirect(models.Model):
    subdomain = models.ForeignKey('multitenant.Subdomain', related_name='redirects')
    alternate = models.CharField(max_length=255, help_text='Just the subdomain, not the full url.')

    class Meta:
        verbose_name = _('Subdomain Redirect')
        verbose_name_plural = _('Subdomain Redirects')

    def __full__(self):
        return '%s.%s' % (self.alternate, self.subdomain.site.domain)

    def __unicode__(self):
        return '%s --> %s' % (
            self.__full__(),
            self.subdomain.__full__()
            )

    @classmethod
    def mapping_dict(cls):
        return {sd.__full__():sd.subdomain.__full__() for sd in cls.objects.all()}


class DevDomainRedirect(DomainRedirect):
    pass

    class Meta:
        verbose_name = _('Dev Domain Redirect')
        verbose_name_plural = _('Dev Domain Redirects')

    def __unicode__(self):
        return '%s --> %s' % (self.alternate, self.site.domain)

    @classmethod
    def mapping_dict(cls):
        return {d.alternate:d.site.domain for d in cls.objects.all()}

    @classmethod
    def create_dev_domain(cls, SiteInstance):
        dev, created = DevDomainRedirect.objects.get_or_create(
            site=SiteInstance,
            alternate='dev-%s' % SiteInstance.domain
            )
        if created:
            print 'DevDomainRedirect created: %s --> %s' % (dev.alternate, SiteInstance.domain)
        else:
            print 'Dev domain: %s - already exists!' % dev.alternate

        return dev
