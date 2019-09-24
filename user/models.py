from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True,verbose_name="編號")
    phone_number = models.CharField(null=True,blank=True,max_length=20,verbose_name="電話號碼")