# from django.urls import path

# from .views import *

# urlpatterns = [
#     path("login",login),
#     path("logout",logout),
#     path("sign_up",sign_up),
# ]

from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]