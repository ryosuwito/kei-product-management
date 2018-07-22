from django.db import models
from database_wilayah.models import Provinsi, Kota, Kecamatan, Kelurahan

class ShippingOrigin(models.Model):
    nama = models.CharField(max_length=200, blank=True, null=True)
    provinsi = models.ForeignKey(Provinsi, null=True, on_delete=models.SET_NULL)
    kota = models.ForeignKey(Kota, null=True, on_delete=models.SET_NULL)
    kecamatan = models.ForeignKey(Kecamatan, null=True, on_delete=models.SET_NULL)
    kelurahan = models.ForeignKey(Kelurahan, null=True, on_delete=models.SET_NULL)
    alamat = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.nama.title()