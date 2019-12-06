from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "phone_number", "foodbank")

class SignUp(LoginRequiredMixin, CreateView):
    model = get_user_model()
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    # template_name = 'signup.html'
    template_name = 'inventory/form.html'

class IndexView(TemplateView):
    template_name = "index.html"
