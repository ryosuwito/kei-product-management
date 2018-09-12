from django.db import models
from membership.models import Member
from .my_purchasing import check_current_purcashing

class Reward(models.Model):
    member = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True)
    current_point = models.IntegerField(blank=True, default=0)
    bonus_purchasing = models.IntegerField(blank=True, default=0)

    def get_current_purchasing(self):
        return check_current_purcashing(self.member.user, self)
