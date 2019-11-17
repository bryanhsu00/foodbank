from .models import *
from django.forms import ModelForm ,formset_factory, BaseFormSet
from django import forms
from django.core import validators
from datetime import datetime

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
        widgets = {
            'foodbank': forms.HiddenInput()
        }

class ContacterForm(ModelForm):
    class Meta:
        model = Contacter
        fields = '__all__'

class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        fields = '__all__'
        widgets = {
            'start_date': DateInput(attrs={'class':'datepicker', 'value': datetime.now().strftime("%Y-%m-%d")}),
            'end_date': DateInput(attrs={'class':'datepicker', 'value': datetime.now().strftime("%Y-%m-%d")}),
            'foodbank': forms.HiddenInput()
        }

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'foodbank': forms.HiddenInput()
        }

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

class SendRecordForm(ModelForm):
    class Meta:
        model = SendRecord
        fields = '__all__'

###

class CreateReceiveForm(ModelForm):
    class Meta:
        model = ReceiveRecord
        fields = ['donator', 'contacter', 'location', 'date'] # ['item', 'quantity']
        widgets = {
            'date': DateInput(attrs={'class':'datepicker', 'value': datetime.now().strftime("%Y-%m-%d")})
        }

    def __init__(self, foodbank_id, *args, **kwargs):
        super(CreateReceiveForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(foodbank_id = foodbank_id)
        self.fields['location'].required = True
        self.fields['donator'].queryset = Donator.objects.filter(foodbank_id = foodbank_id)
        self.fields['donator'].required = True

class ItemReceiveForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="分類", required=False)
    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="物品")
    quantity = forms.IntegerField(label="數量", min_value=1, initial=1)
    expiration_date = forms.DateField(label="有效日期", widget=DateInput(), required=False)

class CreateSendForm(ModelForm):
    class Meta:
        model = SendRecord
        fields = ['household', 'location', 'date']
        widgets = {
            'date': DateInput(attrs={'class':'datepicker', 'value': datetime.now().strftime("%Y-%m-%d")})
        }

    def __init__(self, foodbank_id, *args, **kwargs):
        super(CreateSendForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(foodbank_id = foodbank_id)
        self.fields['location'].required = True
        self.fields['household'].queryset = Household.objects.filter(foodbank_id = foodbank_id)
        self.fields['household'].required = True

class ItemSendForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="分類", required=False)
    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="物品")
    quantity = forms.IntegerField(label="數量", min_value=1, initial=1)