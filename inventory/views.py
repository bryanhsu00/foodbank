from django.db import transaction, connection
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, F, Min
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .utils import *
from .forms import *
from .recordViews import *
from datetime import datetime
import json
from django.contrib import messages
from django.core.exceptions import FieldError

class MyException(Exception):
    pass

chinese_name = {
    "Foodbank":"食物銀行", "Donator":"捐贈者", "Contacter":"單位聯絡人", 
    "Household":"關懷戶", "Location":"據點", "Category":"物品分類", 
    "Measure":"衡量單位", "Item":"物品", "Resource":"庫存",
    "ReceiveRecord":"進貨紀錄", "SendRecord":"出貨紀錄",
}

@login_required
def dashboard(request):
    context = get_base_dict_for_view([])
    context.update({"username" : request.user.username})
    return render(request, 'inventory/dashboard.html', context)

@login_required
def read_resource(request):
    st = 'Resource'
    context = {'model_name': st}
    context.update(get_base_dict_for_view([chinese_name[st]]))
    return render(request, 'inventory/readResource.html', context)

@login_required
def read(request, st):
    model = apps.get_model('inventory', st)
    object_list = []
    m = None
    if getattr(model, "foodbank", False):
        m = model.objects.filter(foodbank_id = request.user.foodbank_id).order_by(F('id').desc())
    elif getattr(model, "location", False):
        l = Location.objects.filter(foodbank_id = request.user.foodbank_id)
        m = model.objects.filter(location__name__in=[i.name for i in l]).order_by(F('id').desc())
    else:
        m = model.objects.all().order_by(F('id').desc())

    context = {'object_list' : readable(m),
                'model_name': st}
    context.update(get_base_dict_for_view([chinese_name[st]]))
    return render(request, 'inventory/read.html', context)

@login_required
def create(request, st):
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
    context.update(get_base_dict_for_view([chinese_name[st]]))
    return render(request, 'inventory/form.html', context)

@login_required
def update(request, st, pk):
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    old_obj = copy.deepcopy(obj)
    if request.FILES:
        form = eval(st + 'Form')(request.POST, request.FILES or None, instance=obj)
    else:
        form = eval(st + 'Form')(request.POST or None, instance=obj)
    if form.is_valid():
        try:
            with transaction.atomic():
                if st == 'SendRecord':
                    Resource.add(old_obj)
                    if Resource.remove(obj) == -1: raise MyException("error")
                elif st =='ReceiveRecord':
                    if Resource.remove(old_obj) == -1 : raise MyException("error")
                    Resource.add(obj)
            form.save()
            return HttpResponseRedirect(reverse('read', args=[st]))

        except MyException:
            messages.error(request, '物品, 據點或數量有誤')
            pass

    context = {'form': form, 'model_name': st, 'pk': pk}
    context.update(get_base_dict_for_view([chinese_name[st]]))
    return render(request, 'inventory/form.html', context)

@login_required
def delete(request, st, pk):
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    if request.method == 'POST':
        if st == 'SendRecord':
            Resource.add(obj)
        elif st =='ReceiveRecord':
            Resource.remove(obj)
        obj.delete()
        return HttpResponseRedirect(reverse('read', args=[st]))
    context = {'object': obj }
    context.update(get_base_dict_for_view([chinese_name[st]]))
    return render(request, 'inventory/delete.html', context)

### api
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

@login_required
def get_statistic_data(request, year, month, day):
    loc_list = [i.id for i in Location.objects.filter(foodbank_id = request.user.foodbank_id)]
    models = ['Resource', 'ReceiveRecord', 'SendRecord']
    result = []
    for name in models:
        model = apps.get_model('inventory', name).objects
        if name == 'ReceiveRecord' or name == 'SendRecord':
            if year != 0:
                model = model.filter(date__year = str(year))
            if month != 0:
                model = model.filter(date__month = str(month))
            if day != 0:
                model = model.filter(date__day = str(day))
        model = model\
            .filter(location__in = loc_list)\
            .values(cname = F('item__category__name'))\
            .annotate(sum = Sum('quantity'))

        result.append(model)

    final = {}
    final['label'] = [i['name'] for i in Category.objects.values()]

    for index, name in enumerate(models):
        final[name] = [0]*len(final['label'])
        for i in result[index]:
            final[name][final['label'].index(i['cname'])] = i['sum']

    rm = []
    for i in range(len(final['label'])):
        if(final['Resource'][i] == 0 and final['ReceiveRecord'][i] == 0 and final['SendRecord'][i] == 0):
            rm.append(i)

    rm.reverse()
    for i in rm:
        for k in final:
            del final[k][i]

    return JsonResponse(final, safe=False)

@login_required
def get_expired(request, date):
    exp_date = datetime.strptime(date, '%Y-%m-%d').date()
    loc_list = [i.id for i in Location.objects.filter(foodbank_id = request.user.foodbank_id)]
    result = Resource.objects.filter(location__in = loc_list)\
                             .filter(expiration_date__lte=(exp_date))\
                             .order_by('expiration_date')
    return JsonResponse(readable(result, flag=True), safe=False)

@login_required
def get_resource(request, loc, cate): #取得據點與分類的庫存
    loc_list = [i.id for i in Location.objects.filter(foodbank_id = request.user.foodbank_id)]
    r = Resource.objects.all().filter(location__in = loc_list)
    if loc != "None": r = r.filter(location = int(loc))
    if cate != "None": r = r.filter(item__category = int(cate))

    r = r.values('item').annotate(
                            rsum = Sum('quantity'), 
                            iname = F('item__name'), 
                            rdate = Min('expiration_date'), 
                            measure = F('item__measure__name')
                        )
    result = []
    for i in r:
        result.append({
            'rsum':  str(i['rsum']) + " " + i['measure'],
            'iname': i['iname'],
            'rdate': i['rdate']
        })

    return JsonResponse({"data" : result}, safe=False)