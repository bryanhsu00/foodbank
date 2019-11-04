from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('get_resource/<str:loc_id>/<str:cate_id>', get_resource, name="get_resource"),
    path('get_items_cate', get_items_cate, name="get_items_cate"),
    path('get_cate', get_cate, name="get_cate"),
    path('get_location', get_location, name="get_location"),
    path('read/Resource', read_resource, name="read_resource"),
    path('create/ReceiveRecord', create_receive_record, name='create_receive_record'),
    path('create/SendRecord', create_send_record, name='create_send_record'),
    path('read/<str:st>', read, name='read'),
    path('create/<str:st>', create, name='create'),
    path('update/<str:st>/<int:pk>', update, name='update'),
    path('delete/<str:st>/<int:pk>', delete, name='delete'),
    path('detail/<str:st>/<int:pk>', detail, name='detail'),
    path('QRcodeScanner', QRcodeScanner, name='QRcodeScanner'),
]