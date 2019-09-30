from django.db.models import *
from django.db import models
from user.models import User

class Agency(models.Model): #捐贈者（單位
    name = CharField(max_length=30)
    contact_person = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email = EmailField(max_length=30, blank=True)
    isFoodBank = BooleanField(default=False)

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
    donation_time = DateTimeField(auto_now=True)
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
    record_time = DateTimeField(auto_now=True)
    note = TextField()

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