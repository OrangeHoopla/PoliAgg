from django.shortcuts import render
from django.conf import settings
import json
import os
from django.http import HttpResponse
from example.models import *
from .filters import OrderFilter
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
    name = username.split(',')
    member = congress.objects.filter(first_name=name[0]).filter(last_name=name[1])
    
    print(member[0])
    bills = member[0].bills.all()
    cosponsored = member[0].cosponsored.all()
    committees = member[0].committee_set.all()
    subcommittees = member[0].sub_committee_set.all()
    #print(bills)
    content = {
        'person' : member[0],
        'bills'  : bills,
        'cosponsored': cosponsored,
        'committees': committees,
        'subcommittees': subcommittees,
    }
    return render(request, 'Landing/user-profile.html',content)

def house(request):
    
    member = congress.objects.filter(house=1).filter(congress_num=116)
    
    
    #print(bills)
    content = {
        'members' : member,
    }
    return render(request, 'Landing/house.html',content)

def senate(request):
    
    member = congress.objects.filter(house=0).filter(congress_num=116)
    
    myFilter = OrderFilter(request.GET, queryset=bill.objects.all())
    orders = myFilter.qs
    #print(bills)
    content = {
        'members' : member,
        'filter' : myFilter,
    }
    return render(request, 'Landing/senate.html',content)

def search(request):
    query = request.GET.get('q')
    first = congress.objects.filter(first_name__icontains=query)
    last = congress.objects.filter(last_name__icontains=query)
    bills = bill.objects.filter(name__icontains=query)
    members = first | last
    content = {
        'people' : members,
        'bills'  : bills,
    }
    return render(request,'Landing/search.html',content)

def state(request,state='default'):
    us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
    
    #print(bills)

    print(state)
    house = congress.objects.filter(state=state,house=1)
    senate = congress.objects.filter(state=state,house=0)
    try:
        print(us_state_abbrev[state])
        
        content = {
            'state' : us_state_abbrev[state],
            'house' : house,
            'senate' : senate,
        }
    except:
        content = {
            'state' : state,
            'house' : house,
            'senate' : senate,
        }

    return render(request, 'Landing/state.html',content)


def statelist(request):

    us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
    
    #print(bills)
    
    
    content = {
        'states' : us_state_abbrev,
    }
    return render(request, 'Landing/states.html',content)
    
