from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import *

def agency_list(request):
    template = 'inventory/agency_list.html'
    agency = Agency.objects.all()
    context = {"object_list": agency}
    return render(request, template, context)

def agency_create(request):
    template = 'inventory/agency_create.html'
    if request.method == 'POST':
        print(request.POST['hello'])

    return render(request, template)


