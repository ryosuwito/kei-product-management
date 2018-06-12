from django.db import models

class Provinsi(models.Model):
    name = models.CharField(max_length=100)

class Kota(models.Model):
    name = models.CharField(max_length=100)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)

class Kecamatan(models.Model):
    name = models.CharField(max_length=100)
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE)

class Kelurahan(models.Model):
    name = models.CharField(max_length=100)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)