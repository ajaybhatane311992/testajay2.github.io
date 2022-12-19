from django.db import models
import datetime

# Create your models here.
class CategoryModel(models.Model):
    cname = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.cname}'

class ProductModel(models.Model):
    Name = models.CharField(max_length=200)
    Price = models.FloatField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.id},{self.Name}'

    @staticmethod
    def get_product_by_id(ids):
        return ProductModel.objects.filter(id__in=ids)

    @staticmethod
    def get_products_by_categoryId(category_id):
        if category_id:
            return ProductModel.objects.filter(category=category_id)
        else:
            return ProductModel.objects.all()

class CustomerModel(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    password = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.id},{self.first_name}'

class OrderModel(models.Model):
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    customer=models.ForeignKey(CustomerModel,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=200,default='')
    phone=models.CharField(max_length=20,default='')
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)


    @staticmethod
    def get_order_by_cid(customer_id):
        return OrderModel.objects.filter(customer=customer_id).order_by('-date')





