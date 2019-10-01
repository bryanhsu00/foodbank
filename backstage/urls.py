from django.urls import path

from .views import *

urlpatterns = [
    path("",redirect_to_index),
    path("index",index),
    path("login",login_page),
    path("agency",agancy_list)
]