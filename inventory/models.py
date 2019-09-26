from django.db.models import *
from django.db import models

class Agency(models.Model): #捐贈者（單位
    name = CharField(max_length=30)
    contact_person = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email = EmailField(max_length=30, blank=True)
    isFoodBank = BooleanField(default=False)

class Individual(models.Model): #捐贈者（個人）
    name = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email = EmailField(max_length=30, blank=True)

class Household(models.Model): #關懷戶
    name = CharField(max_length=30)
    home_number = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email = EmailField(max_length=30, blank=True)
    address = CharField(max_length=50)
    population = IntegerField(default=1)
    start_date = DateField(auto_now=True)
    end_date = DateField()
    need_delivery = BooleanField(default=False)
    authentication_key = CharField(max_length=30, blank=True)
    note = TextField(blank = True)

class Place(models.Model):
    name = CharField(max_length=30)
    agency = ForeignKey(
        Agency,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
    )
    address = CharField(max_length=50)
    note = TextField(blank = True)

class Category(models.Model):
    name = CharField(max_length=30)
    note = TextField(blank = True)

class Measure(models.Model):
    name = CharField(max_length=30)

class Item(models.Model):
    name = CharField(max_length=30)
    category = ForeignKey(
        Category,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    picture = FileField(blank = True)
    note = TextField(blank = True)

class Resource(models.Model):
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    place = ForeignKey(
        Place,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    expiration_date = DateField(blank = True)
    quantity = IntegerField(default=1)
    note = TextField(blank = True)

class DonationRecord(models.Model):
    agency = ForeignKey(
        Agency,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    individual = ForeignKey(
        Individual,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    place = ForeignKey(
        Place,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    quantity = IntegerField(default=1)
    donation_time = DateField(auto_now=True)
    note = TextField(blank = True)

class ExpirationRecord(models.Model):
    agency = ForeignKey(
        Agency,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    quantity = IntegerField(default=1)
    record_date = DateField(auto_now=True)
    note = TextField()

class ReceiveRecord(models.Model):
    household = ForeignKey(
        Household,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    quantity = IntegerField(default=1)
    record_date = DateField(auto_now=True)


