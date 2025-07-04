from django.db import models

from django.contrib.auth.models import AbstractUser
from random import randint
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField()
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True) #one time
    updated = models.DateTimeField(auto_now=True) #each time we updates the product record
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class User(AbstractUser):
    phone=models.IntegerField(default=0)
    is_verified=models.BooleanField(default=False)#After verification it will set to True
    otp=models.CharField(max_length=10,null=True,blank=True)#to store the generated otp in backend table

    def generate_otp(self):
        #for creating random otp number for verification
        otp_number=str(randint(1000,9999))+str(self.id)
        self.otp=otp_number
        self.save()