from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import *
from .utils import *
from .forms import *

def agency_list(request):
    template = 'inventory/agency_list.html'
    dict_for_view = get_base_dict_for_view(["agency"])
    dict_for_view["object_list"] = Agency.objects.all()
    return render(request, template, dict_for_view)

def agency_create(request):
    template = 'inventory/agency_form.html'
    dict_for_view = get_base_dict_for_view(["agency"])
    form = AgencyForm(request.POST or None)
    dict_for_view["form"] = form
    if form.is_valid():
        form.save()
        return redirect('agency_list')
    return render(request, template, dict_for_view)

def agency_update(request, pk):
    template = 'inventory/agency_form.html'
    dict_for_view = get_base_dict_for_view(["agency"])
    agency = get_object_or_404(Agency, pk=pk)
    form = AgencyForm(request.POST or None, instance=agency)
    dict_for_view["form"] = form
    if form.is_valid():
        form.save()
        return redirect('agency_list')
    return render(request, template, dict_for_view)

def agency_delete(request, pk):
    template_name='inventory/agency_confirm_delete.html'
    dict_for_view = get_base_dict_for_view(["agency"])
    agency = get_object_or_404(Agency, pk=pk)
    dict_for_view['object'] = agency
    if request.method == 'POST':
        agency.delete()
        return redirect('agency_list')
    return render(request, template_name, dict_for_view)

def agency_detail(request, pk):
    template_name='inventory/agency_detail.html'
    dict_for_view = get_base_dict_for_view(["agency"])
    agency = get_object_or_404(Agency, pk=pk)
    dict_for_view['object'] = agency    
    return render(request, template_name, dict_for_view)





