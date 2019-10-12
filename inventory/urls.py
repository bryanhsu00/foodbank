from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('read/<str:st>', read, name='read'),
    path('create/<str:st>', create, name='create'),
    path('update/<str:st>/<int:pk>', update, name='update'),
    path('delete/<str:st>/<int:pk>', delete, name='delete'),

    path('QRcodeScanner', QRcodeScanner, name='QRcodeScanner'),
]