from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('agency_list', agency_list, name='agency_list'),
    path('agency_create', agency_create, name='agency_create'),
]