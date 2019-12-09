from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('api/<str:st>', api, name="api"),

    path('get_resource_detail/<int:itemId>/<int:locationId>', get_resource_detail, name="get_resource_detail"),
    path('get_resource/<str:loc>/<str:cate>', get_resource, name="get_resource"),
    path('get_items_cate', get_items_cate, name="get_items_cate"),
    path('get_statistic_data/<int:year>/<int:month>/<int:day>', get_statistic_data, name="get_statistic_data"),
    path('get_expired/<str:date>', get_expired, name="get_expired"),

    path('create/ReceiveRecord', create_receive_record, name='create_receive_record'),
    path('create/SendRecord', create_send_record, name='create_send_record'),

    path('read/Resource', read_resource, name="read_resource"),
    path('create/<str:st>', create, name='create'),
    path('read/<str:st>', read, name='read'),
    path('update/<str:st>/<int:pk>', update, name='update'),
    path('delete/<str:st>/<int:pk>', delete, name='delete'),
]