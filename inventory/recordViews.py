from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.urls import reverse
from django.db import transaction
from .forms import *
from .utils import *
import copy

chinese_name = {
    "ReceiveRecord":"進貨紀錄", "SendRecord":"出貨紀錄"
}

class MyException(Exception):
    pass

@login_required
def create_receive_record(request):
    ItemFormset = formset_factory(ItemReceiveForm, extra=1, formset=ItemReceiveFormSet)

    if request.method == 'GET':
        form = CreateReceiveForm(int(request.user.foodbank_id), request.GET or None)
        formset = ItemFormset()

    elif request.method == 'POST':
        r = request.POST.copy()

        try: r['donator'] = Donator.objects.get(name = r['donator']).id # 把值轉成id
        except: pass

        form = CreateReceiveForm(int(request.user.foodbank_id), r)
        formset = ItemFormset(r)

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
                    r.update(quantity = q + idata['quantity']) # it will update all element in queryset
                ReceiveRecord.objects.create(**pdata, **idata)
            return HttpResponseRedirect(reverse('read', args=['ReceiveRecord']))

    context = {'form': form, 'formset': formset, 'model_name': 'ReceiveRecord'}
    if request.method == 'POST': context.update({'name': request.POST['donator']})
    context.update(get_base_dict_for_view([chinese_name['ReceiveRecord']]))
    return render(request, 'inventory/formset.html', context)

@login_required
def create_send_record(request):
    ItemFormset = formset_factory(ItemSendForm, extra=1, formset=ItemSendFormSet)

    if request.method == 'GET':
        form = CreateSendForm(int(request.user.foodbank_id), request.GET or None)
        formset = ItemFormset()

    elif request.method == 'POST':
        r = request.POST.copy()

        try: r['household'] = Household.objects.get(name = r['household']).id
        except: pass

        form = CreateSendForm(int(request.user.foodbank_id), r)
        formset = ItemFormset(r)

        if form.is_valid() and formset.is_valid():
            pdata = form.cleaned_data
            try:
                with transaction.atomic():
                    for i, f in enumerate(formset):
                        idata = f.cleaned_data
                        idata.pop('category', None)
                        q = idata['quantity']
                        r = Resource.objects\
                            .filter(item=idata['item'], location=pdata['location'])\
                            .order_by(F('expiration_date').asc(nulls_last=True))
                        if r.count() == 0:
                            formset[i].errors['item'] = ['無此物品']  
                            raise MyException('無此物品')
                        for obj in r: # 扣掉庫存
                            if obj == r.reverse()[0] and q > obj.quantity:
                                formset[i].errors['quantity'] = ['數量不足']
                                raise MyException('數量不足') 
                            elif obj.quantity > q:
                                obj.quantity = obj.quantity - q
                                obj.save()
                                SendRecord.objects.create(**pdata, item=idata['item'], quantity=q, expiration_date=obj.expiration_date)
                                break
                            else:
                                q = q - obj.quantity
                                SendRecord.objects.create(**pdata, item=idata['item'], quantity=obj.quantity, expiration_date=obj.expiration_date)
                                obj.delete()

                    return HttpResponseRedirect(reverse('read', args=['SendRecord']))
            except MyException: pass

    context = {'form': form, 'formset': formset, 'model_name': 'SendRecord'}
    if request.method == 'POST': context.update({'name': request.POST['household']})
    context.update(get_base_dict_for_view([chinese_name['SendRecord']]))
    return render(request, 'inventory/formset.html', context)
