from django.db import models
from django.contrib.auth.models import AbstractUser
from inventory.models import FoodBank

class User(AbstractUser):
    id = models.AutoField(primary_key=True,verbose_name="編號")
    phone_number = models.CharField(null=True, blank=True ,max_length=30, verbose_name="手機")
    foodbank = models.ForeignKey(
        FoodBank,
        on_delete = models.SET_NULL,
        blank=True, 
        null=True,
        default=None
    )