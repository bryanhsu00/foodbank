from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import *
from .forms import *
from django.apps import apps
from django.urls import reverse
import collections
import re

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
    context = {'object':obj}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

def convert(dic, model, fields):
    result = collections.OrderedDict()
    fields.insert(0, 'id')
    for key in fields:
        new_key = model._meta.get_field(key).verbose_name
        match = re.search(r'^(.*)_id$', key)
        if match and dic[key] != None:
            result[new_key] = apps.get_model('inventory', 
                match.group(1).capitalize()).objects.get(pk = dic[key]).__str__()
        else:
            result[new_key] = dic[key]
    return result

def QRcodeScanner(request):
    template = "inventory/QRcodeScanner.html"
    return render(request, template, {})
