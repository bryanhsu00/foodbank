from .models import *
from django.forms import ModelForm
from django import forms

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
            'end_date': DateInput()
        }

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

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

class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'

class ReceiveRecordForm(ModelForm):
    class Meta:
        model = ReceiveRecord
        fields = '__all__'

class ExpirationRecordForm(ModelForm):
    class Meta:
        model = ExpirationRecord
        fields = '__all__'

class SendRecordForm(ModelForm):
    class Meta:
        model = SendRecord
        fields = '__all__'