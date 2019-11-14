from django.db import transaction, connection
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.urls import reverse
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from .utils import *
from .forms import *
import json

class MyException(Exception):
    pass

@login_required
def index(request):
    print(request.user.foodbank_id)
    d = get_base_dict_for_view(["index"])
    l = []
    for i in apps.get_models():
        if i._meta.app_label == 'inventory':
            l.append(i._meta.object_name)
    d['model_list'] = l
    return render(request, 'inventory/index.html', d)

@login_required
def read_resource(request):
    template = 'inventory/readResource.html'
    st = 'Resource'
    context = {'model_name': st}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

@login_required
def create_receive_record(request):
    ItemFormset = formset_factory(ItemReceiveForm, extra=1)
    template = 'inventory/formset.html'
    name = None 
    if request.method == 'GET':
        form = CreateReceiveForm(int(request.user.foodbank_id), request.GET or None)
        formset = ItemFormset()
        
    elif request.method == 'POST':
        r = request.POST.copy()
        name = r['donator'] # 取得input值

        try:
            r['donator'] = Donator.objects.get(name = r['donator']).id # 把值轉成id
        except:
            pass

        form = CreateReceiveForm(int(request.user.foodbank_id), r)
        formset = ItemFormset(r)
        try:
            if form.is_valid() and formset.is_valid():
                ### 檢查開始
                for i, f in enumerate(formset):
                    idata = f.cleaned_data
                    if 'item' not in idata:
                        formset[i].errors['item'] = ['這個欄位是必須的']
                        raise MyException("no this kind of choice")
                ### 檢查結束
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
        except MyException:
            pass
    context = {'form': form, 'formset': formset, 'model_name': 'ReceiveRecord'}
    if request.method == 'POST':
        context.update({'name': name})
    context.update(get_base_dict_for_view(['ReceiveRecord']))
    return render(request, template, context)

@login_required
def create_send_record(request):
    ItemFormset = formset_factory(ItemSendForm, extra=1)
    template = 'inventory/formset.html'
    name = None
    if request.method == 'GET':
        form = CreateSendForm(int(request.user.foodbank_id), request.GET or None)
        formset = ItemFormset()
    elif request.method == 'POST':
        r = request.POST.copy()
        name = r['household']

        try:
            r['household'] = Household.objects.get(name = r['household']).id
        except:
            pass

        form = CreateSendForm(int(request.user.foodbank_id), r)
        formset = ItemFormset(r)
        if form.is_valid() and formset.is_valid():
            pdata = form.cleaned_data
            try:
                with transaction.atomic():
                    for i, f in enumerate(formset):
                        idata = f.cleaned_data # item data
                        idata.pop('category', None)
                        if 'item' not in idata:
                            formset[i].errors['item'] = ['這個欄位是必須的']  
                            raise MyException("This filed is necessary!")
                        q = idata['quantity']
                        r = Resource.objects\
                            .filter(item=idata['item'], location=pdata['location'])\
                            .order_by(F('expiration_date').asc(nulls_last=True))
                        if r.count() == 0:
                            formset[i].errors['item'] = ['無此物品']  
                            raise MyException("No this kind of resources!")
                        for obj in r: # 扣掉庫存
                            if obj == r.reverse()[0] and q > obj.quantity:
                                formset[i].errors['quantity'] = ['數量不足']
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
    if request.method == 'POST':
        context.update({'name': name})
    context.update(get_base_dict_for_view(['SendRecord']))
    return render(request, template, context)

@login_required
def read(request, st):
    model = apps.get_model('inventory', st)
    template = 'inventory/read.html'
    object_list = []
    m = None
    if getattr(model, "foodbank", False):
        m = model.objects.filter(foodbank_id = request.user.foodbank_id).order_by(F('id').desc())
    elif getattr(model, "location", False):
        l = Location.objects.filter(foodbank_id = request.user.foodbank_id)
        m = model.objects.filter(location__name__in=[i.name for i in l]).order_by(F('id').desc())
    else:
        m = model.objects.all().order_by(F('id').desc())
    for i in m:
        object_list.append(convert(i.__dict__, model, model.view_fields()))
    context = {'object_list' : object_list,
                'model_name': st}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

@login_required
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

@login_required
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

@login_required
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

@login_required
def delete(request, st, pk):
    template = 'inventory/delete.html'
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect(reverse('read', args=[st]))
    context = {'object': obj }
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

@login_required
def QRcodeScanner(request):
    template = "inventory/QRcodeScanner.html"
    return render(request, template, {})

@login_required
def api(request, st):
    model = apps.get_model('inventory', st)
    data = None
    if getattr(model, "foodbank", False):
        data = model.objects.filter(foodbank_id = request.user.foodbank_id).values()
    else:
        data = model.objects.values()
    return JsonResponse(list(data), safe=False)

@login_required
def get_items_cate(request): #取得所有的分類跟其對應的商品
    res = {}
    l = list(Item.objects.all().values("id", "name", "category_id"))
    for d in l:
        if d['category_id'] in res:
            res[d['category_id']].append({'id':d['id'], 'name':d['name']})
        else:
            res[d['category_id']] = [{'id':d['id'], 'name':d['name']}]
    return JsonResponse(res)

def get_static_data(request):
    ReceiveRecord.objects.all().values("")

@login_required
def get_resource(request, loc_id, cate_id): #取得據點與分類的庫存
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

    sql3 = "group by {}resource.item_id order by {}resource.id desc".format('inventory_', 'inventory_')

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

