from django.contrib import admin
from .models import ProductModel,CategoryModel,CustomerModel,OrderModel

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','Name','Price','category','description','image']
admin.site.register(ProductModel,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cname']
admin.site.register(CategoryModel,CategoryAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','phone','password']
admin.site.register(CustomerModel,CustomerAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','product','customer','quantity','price','address','phone','date','status']
admin.site.register(OrderModel,OrderAdmin)
