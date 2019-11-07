from django.db import transaction, connection
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.urls import reverse
from django.forms import formset_factory
from .utils import *
from .forms import *
import json

class MyException(Exception):
    pass

def index(request):
    print(request.user.foodbank_id)
    d = get_base_dict_for_view(["index"])
    l = []
    for i in apps.get_models():
        if i._meta.app_label == 'inventory':
            l.append(i._meta.object_name)
    d['model_list'] = l
    return render(request, 'inventory/index.html', d)

def read_resource(request):
    template = 'inventory/readResource.html'
    st = 'Resource'
    context = {'model_name': st}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

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
                                obj.quantity = obj.quantity - q
                                obj.save()
                                break
                            else:
                                q = q - obj.quantity
                                obj.delete()
                        SendRecord.objects.create(**pdata, **idata)
                    return HttpResponseRedirect(reverse('read', args=['SendRecord']))
            except MyException:
                pass
    context = {'form': form, 'formset': formset, 'model_name': 'SendRecord'}
    context.update(get_base_dict_for_view(['SendRecord']))
    return render(request, template, context)

def read(request, st):
    model = apps.get_model('inventory', st)
    template = 'inventory/read.html'
    object_list = []
    m = None
    if getattr(model, "foodbank", False):
        m = model.objects.filter(foodbank_id = request.user.foodbank_id)
    elif getattr(model, "location", False):
        l = Location.objects.filter(foodbank_id = request.user.foodbank_id)
        m = model.objects.filter(location__name__in=[i.name for i in l])
    else:
        m = model.objects.all()
    for i in m:
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
        instance = form.save(commit = False)
        instance.foodbank_id = int(request.user.foodbank_id)
        instance.save()
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
    context = {
                'pk': pk, 
                'model_name': st, 
                'obj': convert(obj.__dict__, model, model.all_fields())
            }
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

def get_cate(request):
    data =list(Category.objects.values())
    return JsonResponse(data, safe=False)

def get_location(request):
    data =list(Location.objects.filter(foodbank_id = request.user.foodbank_id).values())
    print(data)
    return JsonResponse(data, safe=False)

def get_resource(request, loc_id, cate_id):
    lst = Location.objects.filter(foodbank_id = request.user.foodbank_id)
    strLst = str([i.id for i in lst]).replace('[','(').replace(']',')')

    sql1 = '''
        select {}resource.*, {}category.name, {}category.id as cid, \
        sum({}resource.quantity) as rsum, {}item.name as iname,\
        min({}resource.expiration_date) as rdate \
        from {}resource, {}category, {}item \
        where {}resource.item_id = {}item.id and \
        {}item.category_id = {}category.id and \
        {}resource.location_id in {} \
        '''.format(*['inventory_']*14, strLst)

    sql2 = ""
    if loc_id != "None":
        sql2 += "and {}resource.location_id = {} ".format('inventory_', loc_id)
    if cate_id != "None":
        sql2 += "and {}category.id = {} ".format('inventory_', cate_id)

    sql3 = "group by {}resource.item_id".format('inventory_')

    sql = sql1 + sql2 + sql3
    c = connection.cursor()
    res = c.execute(sql)
    descibe = []
    dict_list = []
    for i in res.description:
        descibe.append(i[0])
    for i in res.fetchall():
        d = {}
        for index, content in enumerate(i):
            d[descibe[index]] = content
        dict_list.append(d)
    
    return JsonResponse({"data":dict_list}, safe=False)

    