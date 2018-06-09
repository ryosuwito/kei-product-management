from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length= 100)
    description = models.TextField(blank=True)
    is_archived = models.BooleanField(default = False) 

class Product(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length = 150)
    description = models.TextField()
    photo = models.ImageField(upload_to = 'product_photo')
    price = models.IntegerField()
    unit_weight = models.IntegerField()
    product_available = models.BooleanField(default = True)
    is_archived = models.BooleanField(default = False)
    categories = models.ManyToManyField(Category, related_name="category")
    