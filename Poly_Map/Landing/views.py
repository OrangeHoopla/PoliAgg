from django.shortcuts import render
from django.conf import settings
import json
import os
from django.http import HttpResponse
from example.models import *
# Create your views here.
# website name poliagr







def home(request):
    f=os.path.join( settings.BASE_DIR, 'Landing/static/senate.json' )
    with open(f, 'r') as f:
        datastore = json.load(f)
        test = {}
    
    context = {
        'posts': datastore,
        'demos':test,
    }
    return render(request, 'Landing/Land.html', context)


def home2(request,username='default'):
	name = username.split('.')
	member = congress.objects.filter(first_name=name[0]).filter(last_name=name[1])
	print(member[0])
	content = {
		'person' : member[0]
	}
	return render(request, 'Landing/user-profile.html',content)
    
