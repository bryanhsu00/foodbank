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
        object_list.append(convert(i.__dict__, model, model.get_limit()))
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
    context = {'pk': pk, 'model_name': st, 'obj': convert(obj.__dict__, model)}
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

def convert(d, model, limit = None):
    if limit:
        for key, val in d.copy().items():
            if key not in limit and key != 'id':
                del d[key]
    new_d = {}
    for key, val in d.items():
        if key == '_state': 
            continue
        new_k = model._meta.get_field(key).verbose_name
        match = re.search(r'^(.*)_id$', key)
        if match and val != None:        
            new_d[new_k] = apps.get_model('inventory', match.group(1)
                .capitalize()).objects.get(pk = val).__str__()
        else:
            new_d[new_k] = val
    return new_d

def QRcodeScanner(request):
    template = "inventory/QRcodeScanner.html"
    return render(request, template, {})
