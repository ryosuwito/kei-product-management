from django.db import models
from django_extensions.db.fields import AutoSlugField

class Category(models.Model):
    name = models.CharField(db_index=True,
            max_length = 100,
            help_text="Nama Kategori")
    slug = AutoSlugField(max_length=100, 
            unique=True, 
            db_index=True,
            populate_from=('name',))
    description = models.TextField(blank=True,
            help_text="Deskripsi Kategori")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Kategori") 

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
       return self.name

class Product(models.Model):
    name = models.CharField(max_length = 200,
            db_index=True,
            help_text="Nama Produk")
    slug = AutoSlugField(max_length=100, 
            db_index=True,
            unique=True, 
            populate_from=('name',))
    description = models.TextField(help_text="Deskripsi Produk")
    photo = models.ImageField(upload_to = 'product_photo',
            help_text="Foto Produk")
    price = models.IntegerField(help_text="Harga Produk")
    unit_weight = models.IntegerField(help_text="Berat Satuan Produk dalam gram")
    product_available = models.BooleanField(default = True,
            help_text="Centang Jika Produk Tersedia")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Produk")
    categories = models.ManyToManyField(Category, 
            related_name="category",
            help_text="Kategori Produk")

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
       return self.name
    