from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.apps import apps
import re, collections
from django.db.models import F

english_name = {
    "食物銀行":"read/Foodbank", "捐贈者":"read/Donator", "單位聯絡人":"read/Contacter", 
    "關懷戶":"read/Household", "據點":"read/Location", "物品分類":"read/Category", 
    "衡量單位":"read/Measure", "物品":"read/Item", "庫存":"read/Resource", 
    "進貨紀錄":"read/ReceiveRecord", "出貨紀錄":"read/SendRecord"
    }

def readable(query_set, flag=None):
    result = []
    names = [
                {
                    "name" : i.name, 
                    "verbose_name" : i.verbose_name, 
                    "is_relation" : i.is_relation, 
                    "choices" : i.choices 
                } for i in query_set.model._meta.fields
            ]
    for q in query_set: # dict 陣列
        tmp = collections.OrderedDict()
        for n in names:
            field_name = n["verbose_name"]
            field_value = None
            if n['is_relation']: # is fk
                obj = getattr(q, n['name'], None)
                if obj != None:
                    field_value = obj.name
            elif n['choices'] != []:
                field_value = getattr(q, "get_"+n['name']+"_display")()
            else:
                field_value = getattr(q, n['name'])
            tmp[field_name] = field_value
        result.append(tmp)

    model_name = query_set.model.__name__
    if model_name in ['ReceiveRecord', 'SendRecord'] or flag == True:
        for q, r in zip(query_set
                        .annotate(measure=F('item__measure__name'))
                        .values("measure"), 
                        result):
            r.update(q)
    return result

def get_extend_breadcrumb_items(items_array):
    extend_breadcrumb_items = []
    for i in range(len(items_array)):
        tmp_string = ""
        for j in range(i+1):
            tmp_string += items_array[j]
        extend_breadcrumb_items.append({
            "title" : items_array[i],
            "link" : settings.INVENTORY_ROOT + english_name[tmp_string],
            "isActive" : False,
        })
    # extend_breadcrumb_items[-1]["isActive"] = True
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
    category = [{
            "title" : "庫存管理",
            "app" : [
                {
                    "name" : "物品管理",
                    "icon" : "free_breakfast", #gogole icon
                    "isDropdown" : True, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "庫存",
                            "link" : settings.INVENTORY_ROOT+"read/Resource",
                            "icon" : "save_alt", 
                        },
                        {
                            "title" : "物品",
                            "link" : settings.INVENTORY_ROOT+"read/Item",
                            "icon" : "free_breakfast", 
                        },
                        {
                            "title" : "物品分類",
                            "link" : settings.INVENTORY_ROOT+"read/Category",
                            "icon" : "format_list_bulleted", 
                        },
                        {
                            "title" : "衡量單位",
                            "link" : settings.INVENTORY_ROOT+"read/Measure",
                            "icon" : "format_list_bulleted", 
                        }
                    ]
                },
                {
                    "name" : "紀錄管理",
                    "icon" : "subject", #gogole icon
                    "isDropdown" : True, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "進貨紀錄",
                            "link" : settings.INVENTORY_ROOT+"read/ReceiveRecord",
                            "icon" : "subject", 
                        },
                        {
                            "title" : "出貨紀錄",
                            "link" : settings.INVENTORY_ROOT+"read/SendRecord",
                            "icon" : "subject", 
                        },
                        # {
                        #     "title" : "報廢紀錄",
                        #     "link" : settings.INVENTORY_ROOT+"read/ExpirationRecord",
                        #     "icon" : "subject", 
                        # }
                    ]
                },
                {
                    "name" : "人員管理",
                    "icon" : "perm_identity", #gogole icon
                    "isDropdown" : True, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "捐贈者",
                            "link" : settings.INVENTORY_ROOT+"read/Donator",
                            "icon" : "account_box", 
                        },
                        {
                            "title" : "關懷戶",
                            "link" : settings.INVENTORY_ROOT+"read/Household",
                            "icon" : "sentiment_satisfied_alt", 
                        },
                        {
                            "title" : "單位負責人",
                            "link" : settings.INVENTORY_ROOT+"read/Contacter",
                            "icon" : "house", 
                        },
                    ]
                },
                {
                    "name" : "地點管理",
                    "icon" : "house", #gogole icon
                    "isDropdown" : True, #false顯示item第一個
                    "item" : [
                        {
                            "title" : "據點",
                            "link" : settings.INVENTORY_ROOT+"read/Location",
                            "icon" : "house",  
                        },
                        # {
                        #     "title" : "食物銀行",
                        #     "link" : settings.INVENTORY_ROOT+"read/Foodbank",
                        #     "icon" : "house", 
                        # }
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
        # "PROJECT_NAME" : settings.PROJECT_NAME,
        "PROJECT_NAME" : "食物銀行",
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

