from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
import pyqrcode
import os 

class Member(models.Model):
    GUEST = 0
    NEW_MEMBER = 1
    DROPSHIPPER = 2
    RESELLER = 3
    AGEN = 4
    DISTRIBUTOR = 5
    MASTER_SELLER = 6

    LEVEL = {
        'DROPSHIPPER' : {
            'THRESHOLD': 190000,
            'BENEFIT': 5,
        },
        'RESELLER': {
            'THRESHOLD': 1500000,
            'BENEFIT': 10,
        },
        'AGEN': {
            'THRESHOLD': 6800000,
            'BENEFIT': 20,
        },
        'DISTRIBUTOR': {
            'THRESHOLD': 11900000,
            'BENEFIT': 30,
        },
        'MASTER_SELLER': {
            'THRESHOLD': 11900000,
            'BENEFIT': 30,
        }
    }

    USER_TYPE_CHOICES = (
        (GUEST, 'Guest'),
        (NEW_MEMBER, 'New Member'),
        (DROPSHIPPER, 'Dropshipper'),
        (RESELLER, 'Reseller'),
        (AGEN, 'Agen'),
        (DISTRIBUTOR, 'Distributor'),
        (MASTER_SELLER, 'Master Seller'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE) #done
    sponsor_code = models.CharField(db_index=True, max_length=12, blank=True) #done
    referal_code = models.CharField(db_index=True, max_length=12, blank=True) #done
    sponsor = models.ForeignKey(User, on_delete=models.SET_NULL, db_index=True,  related_name="sponsor", null=True) #done
    member_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=NEW_MEMBER) #done
    phone_regex = RegexValidator(regex=r'^\+?62?\d{9,15}$', message="Nomor Telepon Harus memiliki format +62819999999 atau 0819999999'. Maksimal 15 Digit.")
    phone_number = models.CharField(unique=True, validators=[phone_regex], max_length=17, blank=True) # validator haruslah berupa list
    ktp_address = models.CharField(max_length=250, blank=True)
    home_address = models.CharField(max_length=250, blank=True)
    ktp_number = models.CharField(max_length=30, null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    bank_name = models.CharField(max_length=50, blank=True)
    bank_book_photo = models.ImageField(upload_to = 'bank_book_photo', blank=True)
    ktp_photo = models.ImageField(upload_to = 'ktp_photo', blank=True)
    profile_photo = models.ImageField(upload_to = 'profile_photo', blank=True)

    instagram_address = models.CharField(max_length=250, blank=True)
    facebook_address = models.CharField(max_length=250, blank=True)
    twitter_address = models.CharField(max_length=250, blank=True)
    line_address = models.CharField(max_length=250, blank=True)
    website_address = models.CharField(max_length=250, blank=True)
    whatsapp_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    qrcode = models.CharField(max_length=20, blank=True)  

    smart_motto = models.CharField(max_length=250, blank=True)
    is_archived = models.BooleanField(default=False)
    is_member_activated = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return ("membership:profile", [self.user.username,])

    def get_ktp_url(self):
        return ("/media/%s"%self.ktp_photo)

    def get_profile_photo_url(self):
        return ("/media/%s"%self.profile_photo)

    def get_bank_url(self):
        return ("/media/%s"%self.bank_book_photo)

    def get_full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_referal():
        referal_code_alpha = get_random_string(5, 
            allowed_chars='0123456789')
        referal_code_beta = get_random_string(4, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        referal_code = '%s%s'%(referal_code_alpha, referal_code_beta)
        if Member.objects.filter(referal_code= referal_code).exists():
            get_referal()
        else:
            return 'KSK{}'.format(referal_code)

    def get_qrcode(content='0123456789AB', name='default'):
        qr = pyqrcode.create('https://%s.localhost:8000/store/'%content)
        filename = "media/%s_%s.png"%(content,name)
        qr.png(filename, scale=12)
        return filename

    def get_level(self):
        if self.member_type == self.DROPSHIPPER :
            level = self.LEVEL['DROPSHIPPER'] 
        if self.member_type == self.RESELLER :
            level = self.LEVEL['RESELLER']
        if self.member_type == self.AGEN :
            level = self.LEVEL['AGEN']
        if self.member_type == self.DISTRIBUTOR :
            level = self.LEVEL['DISTRIBUTOR']
        if self.member_type == self.MASTER_SELLER :
            level = self.LEVEL['MASTER_SELLER']
        return level

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        member = Member(user=instance)
        member.referal_code = Member.get_referal();
        member.qrcode = Member.get_qrcode(name=member.referal_code,
            content=instance.username);
        member.save()
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.member.save()
