from datetime import datetime
from django.db import models
from rest_framework.relations import PrimaryKeyRelatedField
import time
from user.models import User


class Book(models.Model):
    product_code = models.CharField(max_length=262,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    tax = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.product_code
    class Meta:
        verbose_name_plural = "Books"    
class SuggestedBooks(models.Model):
    suggester = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book,blank=True,verbose_name="Books")
    advisory = models.TextField(blank=True)
    def __str__(self):
        return self.suggester.username
    class Meta:
        verbose_name_plural = "Suggested Books"    


class Classes(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    class_name = models.CharField(max_length=700,null=True,blank=True)
    class_number = models.IntegerField()
    keycode = models.CharField(max_length=4)
    books = models.ManyToManyField(Book,null=True,blank=True)
    class Meta:
        ordering = ['created_at']
        
        verbose_name_plural = "Classes"
    def __str__(self):
        return self.class_name
    
class School(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    logo = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=700,null=True,blank=True)
    
    city = models.CharField(max_length=45)
    country = models.CharField(max_length=100)
    classesq = models.ManyToManyField(Classes,null=True,blank=True)
    class Meta:
        verbose_name_plural = "Schools"
        ordering = ['created_at']
    def __str__(self):
        return self.name 

