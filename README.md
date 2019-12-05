# food_bank

![Python Version](https://img.shields.io/badge/Python-3.6-green.svg)
![Django Version](https://img.shields.io/badge/django-2.2.4-green.svg)

## 結構

```
├── db.sqlite3
├── foodbank
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── inventory
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py
│   ├── recordViews.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── manage.py
├── media
│   ├── images/
│   └── pci.jpg
├── README.md
├── remove_cache.py
├── runserver.py
├── server.py
├── static/
├── stopserver.py
├── templates
│   ├── 404.html
│   ├── 500.html
│   ├── backstage/
│   ├── home.html
│   ├── inventory
│   │   ├── delete.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   ├── formset.html
│   │   ├── index.html
│   │   ├── read.html
│   │   └── readResource.html
│   ├── message.html
│   ├── registration
│   │   └── login.html
│   └── signup.html
└── user
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations/
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py

```
## 套件

```
├── Django
├── django-widget-tweaks 
```

## 備註

1. push 前可以先執行 remove_cache.py
2. setting 中 DEBUG 設為 False 後可以執行 runserver.py 啟動伺服器

## 代辦事項

1.  填表單若沒有這個選項（新增選項後跳回原本表單)
2.  單位負責人要篩選
3.  物品名稱顯示數量固定
4.  demo網址不用輸入帳號密碼

## 備註(12/2) :
1. 出貨紀錄 -> 修改 -> 領取據點會多出愛蘭倉庫
2. 單位聯絡人的新增 -> 所屬單位能不能只顯示團體或食物銀行?
3. 進貨 -> 當捐贈者是個人 -> 不能選擇單位連絡人(可以選的話會錯亂) 
4. 進貨 -> 捐贈者是團體時 -> 單位連絡人要能連動
5. 數量排序規則自訂
