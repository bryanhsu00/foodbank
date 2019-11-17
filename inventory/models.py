from django.db.models import *
from django.utils import timezone
from django.core.validators import MinValueValidator

class FoodBank(Model):
    name = CharField(max_length=30, verbose_name='名稱')
    home_number = CharField(max_length=30, blank=True, verbose_name='市話')
    email = EmailField(max_length=30, blank=True, verbose_name='email')
    address = CharField(max_length=50, blank=True, verbose_name='地址')

    @staticmethod
    def view_fields():
        return ['name', 'home_number']

    @staticmethod
    def all_fields():
        return ['name', 'home_number', 'email', 'address']

    def __str__(self):
        return self.name

class Donator(Model):
    name = CharField(max_length=30, verbose_name='名稱')
    phone_number = CharField(max_length=30, blank=True, verbose_name='手機')
    home_number = CharField(max_length=30, blank=True, verbose_name='市話')
    email = EmailField(max_length=30, blank=True, verbose_name='email')
    pattern = CharField(
        max_length=10,
        choices=[ 
                    ('Individual', '個人'),
                    ('Agency', '團體'),
                    ('FoodBank', '食物銀行')
                ],
        default='Individual',
        verbose_name='類型'
    )
    foodbank = ForeignKey(
        FoodBank,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name="食物銀行"
    )

    @staticmethod
    def view_fields():
        return ['name', 'phone_number']

    @staticmethod
    def all_fields():
        return ['name', 'phone_number', 'home_number', 'email', 'pattern']

    def __str__(self):
        return self.name
    
class Contacter(Model):
    donator = ForeignKey(
        Donator,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='所屬單位'
    )
    name = CharField(max_length=30, verbose_name='姓名')
    phone_number = CharField(max_length=30, blank=True, verbose_name='手機')

    @staticmethod
    def view_fields():
        return ['donator_id', 'name', 'phone_number']

    @staticmethod
    def all_fields():
        return ['donator_id', 'name', 'phone_number']

    def __str__(self):
        return self.name

    
class Household(Model): #關懷戶
    name = CharField(max_length=30, verbose_name='名稱')
    phone_number = CharField(max_length=30, blank=True, verbose_name='手機')
    home_number = CharField(max_length=30, blank=True, verbose_name='市話')
    address = CharField(max_length=50, blank=True, verbose_name='地址')
    population = PositiveIntegerField(default=1, verbose_name='人數', validators=[MinValueValidator(1)])
    start_date = DateField(blank=True, null=True, verbose_name='開始日期')
    end_date = DateField(blank=True, null=True, verbose_name='結束日期')
    # need_delivery = BooleanField(default=False, verbose_name='配送')
    authentication_key = CharField(max_length=30, blank=True, verbose_name='識別碼')
    foodbank = ForeignKey(
        FoodBank,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name="食物銀行"
    )

    @staticmethod
    def view_fields():
        return ['name', 'phone_number']

    @staticmethod
    def all_fields():
        return ['name', 'phone_number', 'home_number', 'address', 'population', 
        'start_date', 'end_date', 'authentication_key']

    def __str__(self):
        return self.name

class Location(Model): #據點
    name = CharField(max_length=30, verbose_name='名稱')
    foodbank = ForeignKey(
        FoodBank,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name="食物銀行"
    )
    address = CharField(max_length=50, blank=True, verbose_name='地址')

    @staticmethod
    def view_fields():
        return ['name', 'address']
    
    @staticmethod
    def all_fields():
        return ['name', 'foodbank_id', 'address']

    def __str__(self):
        return self.name

class Category(Model): #分類
    name = CharField(max_length=30, verbose_name='分類')

    @staticmethod
    def view_fields():
        return ['name']

    @staticmethod
    def all_fields():
        return ['name']

    def __str__(self):
        return self.name

class Measure(Model): #衡量單位
    name = CharField(max_length=30, verbose_name='單位')

    @staticmethod
    def view_fields():
        return ['name']
    
    @staticmethod
    def all_fields():
        return ['name']

    def __str__(self):
        return self.name

class Item(Model): #物品名稱
    name = CharField(max_length=30, verbose_name='物品名稱')
    category = ForeignKey(
        Category,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='物品分類'
    )
    measure = ForeignKey(
        Measure,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='單位'
    )
    picture = ImageField(blank = True, upload_to='images/', verbose_name="照片")

    @staticmethod
    def view_fields():
        return ['name', 'category_id', 'measure_id']
    
    @staticmethod
    def all_fields():
        return ['name', 'category_id', 'measure_id', 'picture']
        
    def __str__(self):
        return self.name

class Resource(Model): #庫存
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='物品名稱',
    )
    location = ForeignKey(
        Location,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
	    verbose_name='據點'
    )
    quantity = IntegerField(default=1, verbose_name='數量')
    expiration_date = DateField(blank=True, null=True, verbose_name='有效日期')

    @staticmethod
    def view_fields():
        # return ['item_id', 'quantity']
        return ['item_id', 'location_id', 'expiration_date', 'quantity']
    
    @staticmethod
    def all_fields():
        return ['item_id', 'location_id', 'expiration_date', 'quantity']

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.item, self.location, self.quantity, self.expiration_date)

class ReceiveRecord(Model): #進貨紀錄
    donator = ForeignKey(
        Donator,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='捐贈者'
    )
    contacter = ForeignKey(
        Contacter,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name="單位聯絡人"
    )
    location = ForeignKey(
        Location,
        on_delete = SET_NULL,
        blank=True, 
        null=True, 
        verbose_name="捐贈據點"
    )
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='物品名稱'
    )
    quantity = IntegerField(default=1, verbose_name='數量')
    date = DateField(blank=True, null=True ,verbose_name="捐贈日期")

    @staticmethod
    def view_fields():
        return ['donator_id', 'item_id', 'quantity']
    
    @staticmethod
    def all_fields():
        return ['donator_id', 'contacter_id', 'location_id', 
        'item_id', 'quantity', 'date']

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.donator, 
                                self.location, self.item, self.quantity, )

class SendRecord(Model): #出貨紀錄
    household = ForeignKey(
        Household,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='關懷戶'
    )
    item = ForeignKey(
        Item,
        on_delete = SET_NULL,
        blank=True, 
        null=True,
        verbose_name='物品名稱'
    )
    quantity = IntegerField(default=1, verbose_name='數量')
    
    location = ForeignKey(
        Location,
        on_delete = SET_NULL,
        blank=True, 
        null=True, 
        verbose_name="領取據點"
    )
    date = DateField(blank=True, null=True, verbose_name="領取日期")
    
    @staticmethod
    def view_fields():
        return ['household_id', 'item_id', 'quantity']
    
    @staticmethod
    def all_fields():
        return ['household_id', 'item_id', 'quantity', 'location_id', 'date']

# class ExpirationRecord(Model): #報廢紀錄
#     item = ForeignKey(
#         Item,
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True, 
#         verbose_name='物品名稱'
#     )
#     quantity = IntegerField(default=1, verbose_name='數量')
#     location = ForeignKey(
#         Location,
#         on_delete = SET_NULL,
#         blank=True, 
#         null=True, 
#         verbose_name="據點"
#     )
#     record_time = DateField(default=timezone.now, blank=True, verbose_name='有效期限')
#     note = TextField(blank=True, verbose_name="備註")

#     @staticmethod
#     def view_fields():
#         return ['item_id', 'quantity', 'record_time']    
    
#     @staticmethod
#     def all_fields():
#         return ['item_id', 'quantity', 'location_id', 'record_time', 'note']

##### 我是分隔線 #####
# class Waybill(Model):
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
#
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
