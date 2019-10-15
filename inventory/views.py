from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import *
from .forms import *
from django.apps import apps
from django.urls import reverse
import collections
import re

def make_dict_ordered(ordered_list, obj_list, st):
    new_list = []
    for obj in obj_list:
        new_obj = collections.OrderedDict()
        for key in ordered_list:
            match = re.search(r'^(.*)_id$', key)
            if match and obj[key] != None:
                new_obj[key] = apps.get_model('inventory', match.group(1)
                                .capitalize()).objects.get(pk = obj[key]).__str__()
            else: 
                new_obj[key] = obj[key]
        new_obj['id'] = obj['id']
        new_list.append(new_obj)
    return new_list

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
    object_list = make_dict_ordered(model.get_field(), model.objects.all().values(), st)
    context = {'object_list' : object_list, 
                'name_list': model.get_verbose(),
                'model_name': st}
    context.update(get_base_dict_for_view([st]))
    return render(request, template, context)

def create(request, st):
    template = 'inventory/form.html'
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
    form = eval(st + 'Form')(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('read', args=[st]))
    context = {'form': form, 'model_name': st}
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



<<<<<<< HEAD
=======
def QRcodeScanner(request):
    template = "inventory/QRcodeScanner.html"
    return render(request, template, {})
    
>>>>>>> 20717c44c9383a2995148252f3ec0d5f9c77a791
