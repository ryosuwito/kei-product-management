from django.contrib import admin
from .models import HeaderLink, FooterLink, HomeLink, Link

class HeaderLinkAdmin(admin.ModelAdmin):
    model = HeaderLink

class FooterLinkAdmin(admin.ModelAdmin):
    model = FooterLink

class HomeLinkAdmin(admin.ModelAdmin):
    model = HomeLink

class LinkAdmin(admin.ModelAdmin):
    model = Link

admin.site.register(HeaderLink, HeaderLinkAdmin)
admin.site.register(FooterLink, FooterLinkAdmin)
admin.site.register(HomeLink, HomeLinkAdmin)
admin.site.register(Link, LinkAdmin)