from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, F
from django.urls import reverse
from django.forms import formset_factory
from .utils import *
from .forms import *
import json

class MyException(Exception):
    pass

def create_receive_record(request):
    ItemFormset = formset_factory(ItemReceiveForm, extra=1)
    template = 'inventory/formset.html'
    if request.method == 'GET':
        form = CreateReceiveForm(request.GET or None)
        formset = ItemFormset()
        
    elif request.method == 'POST':
        form = CreateReceiveForm(request.POST)
        formset = ItemFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            pdata = form.cleaned_data # person data
            for f in formset:
                idata = f.cleaned_data # item data
                idata.pop('category', None) # quantity, item, expire
                r = Resource.objects.filter(
                                            item=idata['item'], 
                                            location=pdata['location'], 
                                            expiration_date=idata['expiration_date']
                                        )
                if r.count() == 0:
                    Resource.objects.create(**idata, location=pdata['location'])
                else:
                    q = r[0].quantity
                    r.update(quantity = q + idata['quantity']) # update all element in queryset
                idata.pop('expiration_date', None)
                ReceiveRecord.objects.create(**pdata, **idata)
            return HttpResponseRedirect(reverse('read', args=['ReceiveRecord']))

    context = {'form': form, 'formset': formset, 'model_name': 'ReceiveRecord'}
    context.update(get_base_dict_for_view(['ReceiveRecord']))
    return render(request, template, context)

def create_send_record(request):
    ItemFormset = formset_factory(ItemSendForm, extra=1)
    template = 'inventory/formset.html'
    if request.method == 'GET':
        form = CreateSendForm(request.GET or None)
        formset = ItemFormset()
    elif request.method == 'POST':
        form = CreateSendForm(request.POST)
        formset = ItemFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            pdata = form.cleaned_data
            try:
                with transaction.atomic():
                    for i, f in enumerate(formset):
                        idata = f.cleaned_data # item data
                        idata.pop('category', None)
                        q = idata['quantity']
                        r = Resource.objects\
                            .filter(item=idata['item'], location=pdata['location'])\
                            .order_by(F('expiration_date').asc(nulls_last=True))
                        if r.count() == 0:
                            formset[i].errors['item'] = ['無此物品！']
                            raise MyException("No this kind of resources!")
                        for obj in r: # 扣掉庫存
                            if obj == r.reverse()[0] and q > obj.quantity:
                                formset[i].errors['quantity'] = ['數量不足！']
                                raise MyException("Not enough resources!") 
                            elif obj.quantity > q:
                                print("2")
                                obj.quantity = obj.quantity - q
                                obj.save()
                                break
                            else:
                                print("3")
                                q = q - obj.quantity
                                obj.delete()
                    return HttpResponseRedirect(reverse('read', args=['SendRecord']))
            except MyException:
                pass
    context = {'form': form, 'formset': formset, 'model_name': 'SendRecord'}
    context.update(get_base_dict_for_view(['SendRecord']))
    return render(request, template, context)

def index(request):
    d = get_base_dict_for_view(["index"])
    l = []
    for i in apps.get_models():
        if i._meta.app_label == 'inventory':
            l.append(i._meta.object_name)
    d['model_list'] = l
    return render(request, 'inventory/index.html', d)

def read(request, st):
    model = apps.get_model('inventory', st)
    template = 'inventory/read.html'
    object_list = []
    for i in model.objects.all():
        object_list.append(convert(i.__dict__, model, model.view_fields()))
    context = {'object_list' : object_list,
                'model_name': st}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

def create(request, st):
    template = 'inventory/form.html'
    if request.FILES:
        form = eval(st + 'Form')(request.POST, request.FILES or None)
    else:
        form = eval(st + 'Form')(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('read', args=[st]))
    context = {'form': form, 'model_name': st}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

def update(request, st, pk):
    template = 'inventory/form.html'
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    if request.FILES:
        form = eval(st + 'Form')(request.POST, request.FILES or None, instance=obj)
    else:
        form = eval(st + 'Form')(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('detail', args=[st, pk]))
    context = {'form': form, 'model_name': st}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

def detail(request, st, pk):
    template = 'inventory/detail.html'
    model = apps.get_model('inventory', st)
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    context = {'pk': pk, 'model_name': st, 'obj': convert(obj.__dict__, model, model.all_fields())}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

def delete(request, st, pk):
    template = 'inventory/delete.html'
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect(reverse('read', args=[st]))
    context = {'object': obj }
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

def QRcodeScanner(request):
    template = "inventory/QRcodeScanner.html"
    return render(request, template, {})


def get_items_cate(request):
    res = {}
    l = list(Item.objects.all().values("id", "name", "category_id"))
    for d in l:
        if d['category_id'] in res:
            res[d['category_id']].append({'id':d['id'], 'name':d['name']})
        else:
            res[d['category_id']] = [{'id':d['id'], 'name':d['name']}]
    return JsonResponse(res)

def get_items_quantity(request, loc_id, item_id):
    location = get_object_or_404(Location, pk = loc_id)
    item = get_object_or_404(Item ,pk = item_id)
    r = Resource.objects\
        .filter(location = location, item = item)\
        .aggregate((Sum('quantity')))
    return JsonResponse(r)
    # print(location, item, quantity)
