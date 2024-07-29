from django.db import models
from ckeditor.fields import RichTextField
import re
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.title
    
class Subcategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title + "------"+ self.category.title
class Brand(models.Model):
    title=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

availability_field=(
    ('in stock', 'in stock'),
    ('out of stock','out of stock'),
    ('pre order','pre order'),
)
class Product(models.Model):
    image=models.ImageField(upload_to='products',blank=True)#pip install pillow
    image2=models.ImageField(upload_to='products',blank=True)
    image3=models.ImageField(upload_to='products',blank=True)
    
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    desc=RichTextField(blank=True)
    Mark_price=models.DecimalField(max_digits=10,decimal_places=2)
    price=models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    discount_percentage=models.DecimalField(max_digits=4,decimal_places=2)
    date=models.DateField(auto_now_add=True)

    availability=models.CharField(choices=availability_field, max_length=50, null=True)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
    
    
    def save(self,*args, **kwargs):
        self.price=self.Mark_price*(1-self.discount_percentage/100)
        self.name=self.name.capitalize()
        self.desc=self.desc=re.sub(r'<[^>]*>', ' ',self.desc)
        super().save(*args, **kwargs)
        
        
    def __str__(self) -> str:
        return self.name


    
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='profile_picture',blank=True,null=True)
    phone_number=models.CharField(max_length=100)
    address=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username



class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    comment=models.TextField()
    rating=models.PositiveIntegerField()
    date=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.name


class Order(models.Model):
    product=models.CharField(max_length=100,default="")
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    price=models.CharField(max_length=100)
    quantity=models.PositiveIntegerField()
    total=models.FloatField()
    image=models.ImageField(upload_to='order/image')
    phone=models.CharField(max_length=12)
    isPay=models.BooleanField(default=False)
    date=models.DateField(default=datetime.now())
    address=models.CharField(max_length=100,default="")

    def __str__(self) -> str:
        return self.product
    
class Transaction(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    transaction_id=models.CharField(max_length=100,null=True)
    amount=models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    created_date=models.DateField(auto_now=True)