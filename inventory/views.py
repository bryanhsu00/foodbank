from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("index")

def out(request):
    return HttpResponse("out")

def store(request):
    return HttpResponse("store")