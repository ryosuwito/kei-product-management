from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Page, Article

def blog_index(request):
    return HttpResponse(Article.objects.all().count())

def page(request, page_slug):
    return HttpResponse(page_slug)

def article(request, article_slug):
    return HttpResponse(article_slug)
