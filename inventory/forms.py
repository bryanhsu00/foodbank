from .models import *
from django.forms import ModelForm

class AgencyForm(ModelForm):
    class Meta:
        model = Agency
        fields = '__all__'

