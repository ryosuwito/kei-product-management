from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

class Member(models.Model):
    GUEST = 0
    NEW_MEMBER = 1
    DROPSHIPPER = 2
    RESELLER = 3
    AGEN = 4
    DISTRIBUTOR = 5
    MASTER_SELLER = 6

    USER_TYPE_CHOICES = (
        (GUEST, 'guest'),
        (NEW_MEMBER, 'new member'),
        (DROPSHIPPER, 'dropshiper'),
        (RESELLER, 'reseller'),
        (AGEN, 'agen'),
        (DISTRIBUTOR, 'distributor'),
        (MASTER_SELLER, 'master seller'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sponsor_code = models.CharField(max_length=12, blank=True)
    referal_code = models.CharField(max_length=12, blank=True)
    sponsor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="member_sponsor", null=True)
    member_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?62?\d{9,15}$', message="Nomor Telepon Harus memiliki format +62819999999 atau 0819999999'. Maksimal 15 Digit.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validator haruslah berupa list
    ktp_address = models.CharField(max_length=250, blank=True)
    home_address = models.CharField(max_length=250, blank=True)
    ktp_number = models.IntegerField(blank=True)
    bank_account_number = models.IntegerField(blank=True)
    bank_name = models.CharField(max_length=10, blank=True)
    bank_book_photo = models.ImageField(upload_to = 'bank_book_photo', blank=True)
    ktp_photo = models.ImageField(upload_to = 'ktp_photo', blank=True)
    profile_photo = models.ImageField(upload_to = 'profile_photo', blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        member = Member(user=instance)
        member.save()
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.member.save()
