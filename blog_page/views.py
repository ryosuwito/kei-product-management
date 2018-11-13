from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from catalog.models import Product

from .models import Page, Article

import random

def blog_index(request):
    return HttpResponse(Article.objects.all().count())

def page(request, page_slug):
    return HttpResponse(page_slug)

def article(request, article_slug):
    article =  get_object_or_404(Article, slug=article_slug)
    all_product = Product.objects.filter(is_archived=False)
    all_article = Article.objects.filter(is_published=True).exclude(slug=article_slug)
    if len(all_product) >= 5:
        other_product = random.sample(list(all_product), 4)
    else:
        other_product = random.sample(list(all_product), len(all_product))

    if len(all_article) >= 4:
        other_article = random.sample(list(all_article), 3)
    else:
        other_article = random.sample(list(all_article), len(all_article))

    return render(request, 'blog_page/blog_detail.html', 
            {"article":article, 
             'other_article':other_article,
             'other_product':other_product})
