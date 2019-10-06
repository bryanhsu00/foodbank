from .models import *
from django.forms import ModelForm

class AgencyForm(ModelForm):
    class Meta:
        model = Agency
        fields = '__all__'

class IndividualForm(ModelForm):
    class Meta:
        model = Individual
        fields = '__all__'

class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        fields = '__all__'

class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        fields = '__all__'

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

class DonationRecordForm(ModelForm):
    class Meta:
        model = DonationRecord
        fields = '__all__'

class ExpirationRecordForm(ModelForm):
    class Meta:
        model = ExpirationRecord
        fields = '__all__'

class ReceiptRecord(ModelForm):
    class Meta:
        model = ReceiptRecord
        fields = '__all__'