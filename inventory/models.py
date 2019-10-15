from django.db.models import *
from django.db import models
from user.models import User
from django.utils import timezone

class Agency(models.Model): #捐贈者（單位)
    name = CharField(max_length=30, verbose_name='單位名稱')
    contact_person = CharField(max_length=30, blank=True, verbose_name='單位負責人')
    phone_number = CharField(max_length=30, blank=True, verbose_name='聯絡電話')
    email = EmailField(max_length=30, blank=True, verbose_name='email')
    is_food_bank = BooleanField(default=False, verbose_name='食物銀行')

    def __str__(self):
        return self.name

    @staticmethod
    def get_verbose():
        return ['單位名稱', '單位負責人', '聯絡電話', 'email', '食物銀行']

    @staticmethod
    def get_field():
        return ['name', 'contact_person', 'phone_number', 'email', 'is_food_bank']
    

class Individual(models.Model): #捐贈者（個人）
    name = CharField(max_length=30, verbose_name='名稱')
    phone_number = CharField(max_length=30, blank=True, verbose_name='手機號碼')
    email = EmailField(max_length=30, blank=True, verbose_name='email')

    def __str__(self):
        return self.name

    @staticmethod
    def get_verbose():
        return ['名稱', '手機號碼', 'email']

    @staticmethod
    def get_field():
        return ['name', 'phone_number', 'email']

class Household(models.Model): #關懷戶
    name = CharField(max_length=30, verbose_name='名稱')
    home_number = CharField(max_length=30, blank=True, verbose_name='家庭號碼')
    phone_number = CharField(max_length=30, blank=True, verbose_name='手機號碼')
    email = EmailField(max_length=30, blank=True, verbose_name='email')
    address = CharField(max_length=50, blank=True, verbose_name='地址')
    population = IntegerField(default=1, verbose_name='人數')
    start_date = DateField(default=timezone.now, blank=True, verbose_name='開始日期')
    end_date = DateField(default=timezone.now, blank=True, verbose_name='結束日期')
    need_delivery = BooleanField(default=False, verbose_name='配送')
    authentication_key = CharField(max_length=30, blank=True, verbose_name='識別碼')
    note = TextField(blank = True, verbose_name='備註')

    def __str__(self):
        return self.name

    @staticmethod
    def get_verbose():
        return ['名稱', '家庭號碼', '手機號碼', 'email', '地址', 
                '人數', '開始日期', '結束日期', '配送', '識別碼', '備註']

    @staticmethod
    def get_field():
        return ['name', 'home_number', 'phone_number', 'email', 'address', 
                'population', 'start_date', 'end_date', 'need_delivery', 
                'authentication_key', 'note']

class Location(models.Model): #據點
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

    @staticmethod
    def get_verbose():
        return ['名稱', '單位', '地址', '備註']

    @staticmethod
    def get_field():
        return ['name', 'agency_id', 'address', 'note']

class Category(models.Model): #分類
    name = CharField(max_length=30)
    note = TextField(blank = True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_verbose():
        return ['名稱', '備註']

    @staticmethod
    def get_field():
        return ['name', 'note']

class Measure(models.Model): #衡量單位
    name = CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def get_verbose():
        return ['名稱']

    @staticmethod
    def get_field():
        return ['name']

class Item(models.Model): #物品
    name = CharField(max_length=30)
    category = ForeignKey(
        Category,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    measure = ForeignKey(
        Measure,
        on_delete = SET_NULL,
        blank=True, 
        null=True
    )
    picture = ImageField(blank = True, upload_to='images/') 
    note = TextField(blank = True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_verbose():
        return ['名稱', '分類', '單位', '照片', '備註']

    @staticmethod
    def get_field():
        return ['name', 'category_id', 'measure_id', 'picture', 'note']

class Resource(models.Model): #可用資源
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

    def __str__(self):
        return '{}, {}, {}'.format(self.item, self.location, self.quantity)

    @staticmethod
    def get_verbose():
        return ['物品', '據點', '有效日期', '數量', '備註']

    @staticmethod
    def get_field():
        return ['item_id', 'location_id', 'expiration_date', 'quantity', 'note']

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

    @staticmethod
    def get_verbose():
        return ['捐贈者（單位)', '捐贈者（個人)', '據點', '物品', '數量', '捐贈時間', '備註']

    @staticmethod
    def get_field():
        return ['agency_id', 'individual_id', 'location_id', 'item_id', 'quantity', 'donation_time', 'note']

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(self.agency, self.individual, self.location,
                                self.item, self.quantity, )

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

    @staticmethod
    def get_verbose():
        return ['據點', '物品', '數量', '紀錄時間', '備註']

    @staticmethod
    def get_field():
        return ['agency_id', 'item_id', 'quantity', 'record_time', 'note']

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

    @staticmethod
    def get_verbose():
        return ['關懷戶', '物品', '數量', '紀錄時間']

    @staticmethod
    def get_field():
        return ['household_id', 'item_id', 'quantity', 'record_time']

##### 我是分隔線 #####
# class Waybill(models.Model):
#     location_import = ForeignKey(
#         Location,
#         related_name='%(class)s_location_import',
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )
#     location_export = ForeignKey(
#         Location,
#         related_name='%(class)s_location_export',
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )
#     agent = ForeignKey(
#         User,
#         related_name='%(class)s_agent',
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )
#     receiver = ForeignKey(
#         User,
#         related_name='%(class)s_receiver',
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )

# class Freight(models.Model):
#     item = ForeignKey(
#         Item,
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )
#     waybill = ForeignKey(
#         Waybill,
#         on_delete="CASCADE",
#         null=False
#     )
#     quantity = IntegerField()

# class RequirementDelivery(models.Model):
#     household = ForeignKey(
#         Household,
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )
#     agent = ForeignKey(
#         User,
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )
#     location_export = ForeignKey(
#         Location,
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True
#     )
#     time_take = DateTimeField()
#     time_receive = DateTimeField()

# class Content(models.Model):
#     requirement_delivery = ForeignKey(
#         RequirementDelivery,
#         on_delete="CASCADE",
#         null=False,
#     )
#     item = ForeignKey(
#         Item,
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True,
#     )
#     quantity = IntegerField()

# class User_Agency(models.Model):
#     user = ForeignKey(
#         User,
#         on_delete="CASCADE",
#         null=False,
#     )
#     agency = ForeignKey(
#         Agency,
#         on_delete="CASCADE",
#         null=False,
#     )

# class DeliveryNote(models.Model):
#     household = ForeignKey(
#         Household,
#         on_delete="CASCADE",
#         null=False,
#     )
#     prefer_day = SmallIntegerField()
#     prefer_period = SmallIntegerField()

# class HouseholdRequirement(models.Model):
#     household = ForeignKey(
#         Household,
#         on_delete="CASCADE",
#         null=False,
#     )
#     note = TextField()