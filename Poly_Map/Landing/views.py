from django.shortcuts import render
from django.conf import settings
import json
import os
# Create your views here.
# website name poliagr







def home(request):
    f=os.path.join( settings.BASE_DIR, 'Landing/static/senate.json' )
    with open(f, 'r') as f:
        datastore = json.load(f)

    
    context = {
        'posts': datastore
    }
    return render(request, 'Landing/Land.html', context)


