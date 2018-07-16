from django.urls import path, re_path
from . import views

app_name = 'storefront'

urlpatterns = [
    path('detail/<int:product_pk>/', views.product_detail, name='product_detail'),
    path('products/', views.product_all, name='product_all'),
    path('products/', views.product_all, name='product_all'),
    re_path(r'$', views.index, name='index'),
]
