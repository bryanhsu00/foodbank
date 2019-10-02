from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('agency_list', agency_list, name='agency_list'),
    path('agency_create', agency_create, name='agency_create'),
    path('agency_update/<int:pk>', agency_update, name='agency_update'),
    path('agency_delete/<int:pk>', agency_delete, name='agency_delete'),
    path('agency_detail/<int:pk>', agency_detail, name='agency_detail')
]