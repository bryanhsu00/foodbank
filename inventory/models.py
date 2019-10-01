from django.db.models import *
from django.db import models
<<<<<<< HEAD
from django.utils import timezone
=======
from user.models import User
>>>>>>> 195d2e15b1afef1100601688c6f5552083a6c842

class Agency(models.Model): #捐贈者（單位)
    name = CharField(max_length=30)
    contact_person = CharField(max_length=30, blank=True)
    phone_number = CharField(max_length=30, blank=True)
    email = EmailField(max_length=30, blank=True)
    is_food_bank = BooleanField(default=False)

    def __str__(self):
        return self.name

class User_Agency(models.Model):
    user = ForeignKey(
        User,
        on_delete="CASCADE",
        null=False,
    )
    agency = ForeignKey(
        Agency,
        on_delete="CASCADE",
        null=False,
    )

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

<<<<<<< HEAD
    def __str__(self):
        return self.name

class Place(models.Model):
=======
class DeliveryNote(models.Model):
    household = ForeignKey(
        Household,
        on_delete="CASCADE",
        null=False,
    )
    prefer_day = SmallIntegerField()
    prefer_period = SmallIntegerField()

class HouseholdRequirement(models.Model):
    household = ForeignKey(
        Household,
        on_delete="CASCADE",
        null=False,
    )
    note = TextField()

class Location(models.Model):
>>>>>>> 195d2e15b1afef1100601688c6f5552083a6c842
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
    picture = ImageField(blank = True)
    note = TextField(blank = True)

class Resource(models.Model):
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    location = ForeignKey(
        Location,
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
    location = ForeignKey(
        Location,
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
<<<<<<< HEAD
    donation_time = DateField(default=timezone.now, blank=True)
=======
    donation_time = DateTimeField(auto_now=True)
>>>>>>> 195d2e15b1afef1100601688c6f5552083a6c842
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
<<<<<<< HEAD
    record_date = DateField(default=timezone.now, blank=True)
    note = TextField(blank=True)
=======
    record_time = DateTimeField(auto_now=True)
    note = TextField()
>>>>>>> 195d2e15b1afef1100601688c6f5552083a6c842

class ReceiptRecord(models.Model):
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
<<<<<<< HEAD
    record_date = DateField(default=timezone.now, blank=True)
    note = TextField(blank = True)
=======
    record_time = DateTimeField(auto_now=True)

class Waybill(models.Model):
    location_import = ForeignKey(
        Location,
        related_name='%(class)s_location_import',
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    location_export = ForeignKey(
        Location,
        related_name='%(class)s_location_export',
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    agent = ForeignKey(
        User,
        related_name='%(class)s_agent',
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    receiver = ForeignKey(
        User,
        related_name='%(class)s_receiver',
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
>>>>>>> 195d2e15b1afef1100601688c6f5552083a6c842

class Freight(models.Model):
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    waybill = ForeignKey(
        Waybill,
        on_delete="CASCADE",
        null=False
    )
    quantity = IntegerField()

class RequirementDelivery(models.Model):
    household = ForeignKey(
        Household,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    agent = ForeignKey(
        User,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    location_export = ForeignKey(
        Location,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    time_take = DateTimeField()
    time_receive = DateTimeField()

class Content(models.Model):
    requirement_delivery = ForeignKey(
        RequirementDelivery,
        on_delete="CASCADE",
        null=False,
    )
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
    )
    quantity = IntegerField()