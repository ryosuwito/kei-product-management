from django.db import models

class Provinsi(models.Model):
    name = models.CharField(db_index=True, max_length=100)

    def __str__(self):
        return self.name

class Kota(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Kecamatan(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Kelurahan(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    postal_code = models.CharField(max_length=20)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    def __str__(self):
        return self.name