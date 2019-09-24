from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('out', views.out, name='index'),
    path('store', views.store, name='index'),
]