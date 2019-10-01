from django.db.models import *
from django.db import models
from django.utils import timezone

class Agency(models.Model): #捐贈者（單位)
    name = CharField(max_length=30)
    contact_person = CharField(max_length=30, blank=True)
    phone_number = CharField(max_length=30, blank=True)
    email = EmailField(max_length=30, blank=True)
    is_food_bank = BooleanField(default=False)

    def __str__(self):
        return self.name

class Individual(models.Model): #捐贈者（個人）
    name = CharField(max_length=30)
    phone_number = CharField(max_length=30, blank=True)
    email = EmailField(max_length=30, blank=True)

    def __str__(self):
        return self.name

class Household(models.Model): #關懷戶
    name = CharField(max_length=30)
    home_number = CharField(max_length=30, blank=True)
    phone_number = CharField(max_length=30, blank=True)
    email = EmailField(max_length=30, blank=True)
    address = CharField(max_length=50, blank=True)
    population = IntegerField(default=1)
    start_date = DateField(default=timezone.now, blank=True)
    end_date = DateField(default=timezone.now, blank=True)
    need_delivery = BooleanField(default=False)
    authentication_key = CharField(max_length=30, blank=True)
    note = TextField(blank = True)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = CharField(max_length=30)
    agency = ForeignKey(
        Agency,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
    )
    address = CharField(max_length=50, blank=True)
    note = TextField(blank = True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = CharField(max_length=30)
    note = TextField(blank = True)

    def __str__(self):
        return self.name

class Measure(models.Model):
    name = CharField(max_length=30)

    def __str__(self):
        return self.name

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
    expiration_date = DateField(default=timezone.now, blank=True)
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
    donation_time = DateField(default=timezone.now, blank=True)
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
    record_date = DateField(default=timezone.now, blank=True)
    note = TextField(blank=True)

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
    record_date = DateField(default=timezone.now, blank=True)
    note = TextField(blank = True)


