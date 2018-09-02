from django.db import models

class Reward(models.Model):
    my_poin = models.IntegerField(blank=True, null=True)
