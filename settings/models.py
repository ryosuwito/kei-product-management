from django.db import models

class Link(models.Model):
    addr = models.SlugField(max_length=400)
    name = models.CharField(max_length=200)

class FooterLink(models.Model):
    link = models.ManyToManyField(Link, 
            related_name="link_in_footer",
            help_text="Link pada footer")

class HeaderLink(models.Model):
    link = models.ManyToManyField(Link, 
            related_name="link_in_header",
            help_text="Link pada header")

class HomeLink(models.Model):
    addr1 = models.SlugField(max_length=400)
    banner1 = models.ImageField(upload_to = 'home_settings',
            help_text="Banner 1")
    addr2 = models.SlugField(max_length=400)
    banner2 = models.ImageField(upload_to = 'home_settings',
            help_text="Banner 2")
    addr3 = models.SlugField(max_length=400)
    banner3 = models.ImageField(upload_to = 'home_settings',
            help_text="Banner 3")
    addr4 = models.SlugField(max_length=400)
    banner1 = models.ImageField(upload_to = 'home_settings',
            help_text="Banner 4")
    addr5 = models.SlugField(max_length=400)
    banner5 = models.ImageField(upload_to = 'home_settings',
            help_text="Banner 5")
    
    addr_sidebar = models.SlugField(max_length=400)
    banner_sidebar = models.ImageField(upload_to = 'home_settings',
            help_text="Banner Sidebar")

    addr_middle = models.SlugField(max_length=400)
    banner_middle = models.ImageField(upload_to = 'home_settings',
            help_text="Banner Middle")