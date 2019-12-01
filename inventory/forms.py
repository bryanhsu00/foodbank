from .models import FoodBank, Contacter, Measure, Resource,\
    Donator, Household, Location, Category, Item, ReceiveRecord, SendRecord
from django.forms import ModelForm ,formset_factory, BaseFormSet
from django import forms
from django.forms import DateField
from django.core import validators
from django.forms import formset_factory

class DateInput(forms.DateInput):
    input_type = 'date'

class FoodBankForm(ModelForm):
    class Meta:
        model = FoodBank
        fields = '__all__'

class DonatorForm(ModelForm):
    class Meta:
        model = Donator
        fields = '__all__'
        widgets = { 'foodbank': forms.HiddenInput() }

class ContacterForm(ModelForm):
    class Meta:
        model = Contacter
        fields = '__all__'

class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        fields = '__all__'
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'foodbank': forms.HiddenInput()
        }

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = { 'foodbank': forms.HiddenInput() }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class MeasureForm(ModelForm):
    class Meta:
        model = Measure
        fields = '__all__'

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

# class ResourceForm(ModelForm):
#     class Meta:
#         model = Resource
#         fields = '__all__'

class ReceiveRecordForm(ModelForm):
    class Meta:
        model = ReceiveRecord
        fields = '__all__'
        widgets = { 'date': DateInput() }

class SendRecordForm(ModelForm):
    class Meta:
        model = SendRecord
        fields = '__all__'
        widgets = { 'date': DateInput() }

### 進貨表單

class CreateReceiveForm(ModelForm):
    class Meta:
        model = ReceiveRecord
        fields = ['donator', 'contacter', 'location', 'date']
        widgets = { 'date': DateInput() }

    def __init__(self, foodbank_id, *args, **kwargs):
        super(CreateReceiveForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(foodbank_id = foodbank_id)
        self.fields['donator'].queryset = Donator.objects.filter(foodbank_id = foodbank_id)

class ItemReceiveForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="分類", required=False)
    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="物品")
    quantity = forms.IntegerField(label="數量", min_value=1, initial=1)
    expiration_date = forms.DateField(label="有效日期", widget=DateInput())

class ItemReceiveFormSet(BaseFormSet):
    def clean(self):
        flag = False
        for index, form in enumerate(self.forms):
            data = form.cleaned_data
            if 'item' not in data:
                flag = True
                self.forms[index].errors['item'] = ['這個欄位是必須的']

            if 'expiration_date' not in data:
                flag = True
                self.forms[index].errors['expiration_date'] = ['這個欄位是必須的']

        if flag:
            raise forms.ValidationError('這個欄位是必須的')

### 出貨表單

class CreateSendForm(ModelForm):
    class Meta:
        model = SendRecord
        fields = ['household', 'location', 'date']
        widgets = { 'date': DateInput() }

    def __init__(self, foodbank_id, *args, **kwargs):
        super(CreateSendForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(foodbank_id = foodbank_id)
        self.fields['household'].queryset = Household.objects.filter(foodbank_id = foodbank_id)

class ItemSendForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="分類", required=False)
    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="物品")
    quantity = forms.IntegerField(label="數量", min_value=1, initial=1)

class ItemSendFormSet(BaseFormSet):
    def clean(self):
        flag = False
        for index, form in enumerate(self.forms):
            data = form.cleaned_data
            if 'item' not in data:
                flag = True
                self.forms[index].errors['item'] = ['這個欄位是必須的']

        if flag:
            raise forms.ValidationError('這個欄位是必須的')