from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site

def index(request):
	return HttpResponse("You're looking at poll")
		



