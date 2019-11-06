# from django.shortcuts import render
# from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
# from django.shortcuts import get_object_or_404

# from django.contrib.auth import authenticate
# from django.contrib import auth
# from django.conf import settings
# from .models import *

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 auth.login(request,user)
#                 return HttpResponse("登入成功")
#     return HttpResponse("登入失敗")

# def logout(request):
#     auth.logout(request)
#     return HttpResponse("已登出") 

# def sign_up(request):
#     username = request.POST.get("username")
#     tmp = User.objects.filter(username=username)
#     if len(tmp) > 0:
#         return HttpResponse("此帳號已經被使用")
#     password = request.POST.get("password")
#     password_check = request.POST.get("password_check")
#     if password != password_check:
#         return HttpResponse("請確認您的密碼")

#     new_user = User.objects.create_user(username=username,password=password)
#     # new_user.is_active = 1 #若無需驗證
#     new_user.save()

#     return HttpResponse("註冊成功")

# from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username","foodbank")

class SignUp(generic.CreateView):

    model = get_user_model()
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'