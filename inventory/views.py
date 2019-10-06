from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import *
from .forms import *
from django.apps import apps
from django.urls import reverse
import collections

def index(request):
    # check, response = check_permission(request)
    # if not check:
    #     return response

    dict_for_view = get_base_dict_for_view(["index"])
    return render(request, 'inventory/index.html', dict_for_view)

def read(request, st):
    st = st.capitalize()
    model = apps.get_model('inventory', st)
    template = 'inventory/read.html'
    object_list = make_dict_ordered(model.get_field(), model.objects.all().values())
    context = {'object_list' : object_list, 
                'name_list': model.get_verbose(),
                'model_name': st}
    return render(request, template, context)

def create(request, st):
    st = st.capitalize()
    template = 'inventory/form.html'
    form = eval(st + 'Form')(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('read', args=[st]))
    return render(request, template, {'form': form, 'model_name': st})

def update(request, st, pk):
    st = st.capitalize()
    template = 'inventory/form.html'
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    form = eval(st + 'Form')(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('read', args=[st]))
    return render(request, template, {'form': form, 'model_name': st})

def delete(request, st, pk):
    st = st.capitalize()
    template = 'inventory/delete.html'
    obj = get_object_or_404(apps.get_model('inventory', st), pk=pk)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect(reverse('read', args=[st]))
    return render(request, template, {'object':obj})

    