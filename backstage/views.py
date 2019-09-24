from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
from .models import *

### 

def get_extend_breadcrumb_items(items_array):
    extend_breadcrumb_items = []
    for i in range(len(items_array)):
        tmp_string = ""
        for j in range(i+1):
            tmp_string += "/"+items_array[j]
        extend_breadcrumb_items.append({
            "title" : items_array[i],
            "link" : settings.BACKSTAGE_ROOT+tmp_string,
            "isActive" : False,
        })
    extend_breadcrumb_items[-1]["isActive"] = True
    return extend_breadcrumb_items

### 設定一次，全部通用
def get_breadcrumb_menu():
    menu = [
        # {
        #     "title" : "Dashboard", 
        #     "link" : "/index",
        # }
    ]
    return menu

def get_side_nav(request):
    category = [
        {
            "title" : "new_project",
            "app" : [
                {
                    "name" : "new_app",
                    "icon" : "subject",
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "new_item",
                            "link" : "#",
                            "icon" : "subject", 
                        }
                    ]
                }
            ]
        }
    ]
    
    side_nav = {
        "category" : category,
    }

    return side_nav


def get_base_dict_for_view(request,extend_breadcrumb_items_array):
    extend_breadcrumb_items = get_extend_breadcrumb_items(extend_breadcrumb_items_array)
    dict_for_view = {
        "PROJECT_NAME" : settings.PROJECT_NAME,
        "BACKSTAGE_ROOT" : settings.BACKSTAGE_ROOT,
        "extend_breadcrumb_items" : extend_breadcrumb_items,
        "breadcrumb_menu" : get_breadcrumb_menu(),
        "side_nav" : get_side_nav(request),
    }
    return dict_for_view

###

def response_404_page(request):
    dict_for_view = {}
    response = render(request, '404.html',dict_for_view)
    return response

def response_500_page(request):
    dict_for_view = {}
    response = render(request, '500.html',dict_for_view)
    return response

def response_message_page(request,message):
    dict_for_view = {
        "message" : message,
    }
    response = render(request, 'message.html', dict_for_view)
    return response

def redirect_to_index(request):
    response = HttpResponseRedirect(settings.BACKSTAGE_ROOT+"/index")
    return response

def index(request):
    # check, response = check_permission(request)
    # if not check:
    #     return response

    extend_breadcrumb_items_array = ["index"]
    dict_for_view = get_base_dict_for_view(request,extend_breadcrumb_items_array)

    response = render(request, 'backstage/index.html',dict_for_view)
    return response

def login_page(request):
    dict_for_view = {
        "PROJECT_NAME" : settings.PROJECT_NAME,
    }
    response = render(request, 'backstage/user/login.html',dict_for_view)
    return response
