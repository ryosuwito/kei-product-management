from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Page, Article

def blog_index(request):
    return HttpResponse(Article.objects.all().count())

def page(request, page_slug):
    return HttpResponse(page_slug)

def article(request, article_slug):
    article =  get_object_or_404(Article, slug=article_slug)
    return render(request, 'blog_page/blog_detail.html', {"article":article})
