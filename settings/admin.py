from django.contrib import admin
from .models import HeaderLink, FooterLink, HomeLink, Link

class HeaderLinkAdmin(admin.ModelAdmin):
    model = HeaderLink
    exclude = ['slug']

class FooterLinkAdmin(admin.ModelAdmin):
    model = FooterLink
    exclude = ['slug']

class HomeLinkAdmin(admin.ModelAdmin):
    model = HomeLink
    exclude = ['slug']

class LinkAdmin(admin.ModelAdmin):
    model = Link
    exclude = ['slug']

admin.site.register(HeaderLink, HeaderLinkAdmin)
admin.site.register(FooterLink, FooterLinkAdmin)
admin.site.register(HomeLink, HomeLinkAdmin)
admin.site.register(Link, LinkAdmin)