from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings

### 

def get_extend_breadcrumb_items(items_array):
    extend_breadcrumb_items = []
    for i in range(len(items_array)):
        tmp_string = ""
        for j in range(i+1):
            tmp_string += "/"+items_array[j]
        extend_breadcrumb_items.append({
            "title" : items_array[i],
            "link" : settings.INVENTORY_ROOT+tmp_string,
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

def get_side_nav():
    category = [
        {
            "title" : "new_project",
            "app" : [
                {
                    "name" : "agency",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "捐贈單位",
                            "link" : settings.INVENTORY_ROOT+"read/Agency",
                            "icon" : "subject",
                        }
                    ]
                },
                {
                    "name" : "individual",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "捐贈個人",
                            "link" : settings.INVENTORY_ROOT+"read/Individual",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "household",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "關懷戶",
                            "link" : settings.INVENTORY_ROOT+"read/Household",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "location",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "據點",
                            "link" : settings.INVENTORY_ROOT+"read/Location",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "category",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "物品分類",
                            "link" : settings.INVENTORY_ROOT+"read/Category",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "measure",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "衡量單位",
                            "link" : settings.INVENTORY_ROOT+"read/Measure",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "item",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "物品",
                            "link" : settings.INVENTORY_ROOT+"read/Item",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "resource",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "庫存",
                            "link" : settings.INVENTORY_ROOT+"read/Resource",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "donation_record",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "進貨紀錄",
                            "link" : settings.INVENTORY_ROOT+"read/DonationRecord ",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "receipt_record",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "出貨紀錄",
                            "link" : settings.INVENTORY_ROOT+"read/ReceiptRecord ",
                            "icon" : "subject", 
                        }
                    ]
                },
                {
                    "name" : "expiration_record",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : False, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "報廢紀錄",
                            "link" : settings.INVENTORY_ROOT+"read/ExpirationRecord ",
                            "icon" : "subject", 
                        }
                    ]
                },
            ]
        }
    ]
    
    side_nav = {
        "category" : category,
    }

    return side_nav


def get_base_dict_for_view(extend_breadcrumb_items_array):
    extend_breadcrumb_items = get_extend_breadcrumb_items(extend_breadcrumb_items_array)
    dict_for_view = {
        "PROJECT_NAME" : settings.PROJECT_NAME,
        "INVENTORY_ROOT" : settings.INVENTORY_ROOT,
        "extend_breadcrumb_items" : extend_breadcrumb_items,
        "breadcrumb_menu" : get_breadcrumb_menu(),
        "side_nav" : get_side_nav(),
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
    response = HttpResponseRedirect(settings.INVENTORY_ROOT+"/index")
    return response

# def login_page(request):
#     dict_for_view = {
#         "PROJECT_NAME" : settings.PROJECT_NAME,
#     }
#     response = render(request, 'inventory/user/login.html',dict_for_view)
#     return response

