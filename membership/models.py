from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Member(models.Model):
    NEW_MEMBER = 1
    DROPSHIPPER = 2
    RESELLER = 3
    AGEN = 4
    DISTRIBUTOR = 5
    MASTER_SELLER = 6

    USER_TYPE_CHOICES = (
        (NEW_MEMBER, 'new member'),
        (DROPSHIPPER, 'dropshiper'),
        (RESELLER, 'reseller'),
        (AGEN, 'agen'),
        (DISTRIBUTOR, 'distributor'),
        (MASTER_SELLER, 'master seller'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sponsor_code = models.CharField(max_length=12)
    referal_code = models.CharField(max_length=12)
    sponsor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="member_sponsor", null=True)
    member_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    phone_regex = RegexValidator(regex=r'^\+?62?\d{9,15}$', message="Nomor Telepon Harus memiliki format +62819999999 atau 0819999999'. Maksimal 15 Digit.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validator haruslah berupa list
    ktp_address = models.CharField(max_length=250)
    home_address = models.CharField(max_length=250)
    ktp_number = models.IntegerField()
    bank_account_number = models.IntegerField()
    bank_name = models.CharField(max_length=100)
    bank_book_photo = models.ImageField(upload_to = 'bank_book_photo')
    ktp_photo = models.ImageField(upload_to = 'ktp_photo')
    profile_photo = models.ImageField(upload_to = 'profile_photo')

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sponsor_code = models.CharField(max_length=12)
    sponsor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="guest_sponsor", null=True)
    home_address = models.CharField(max_length=250)
    phone_regex = RegexValidator(regex=r'^\+?62?\d{9,15}$', message="Nomor Telepon Harus memiliki format +62819999999 atau 0819999999'. Maksimal 15 Digit.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validator haruslah berupa list
 

