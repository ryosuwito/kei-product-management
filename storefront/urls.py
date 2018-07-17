from django.urls import path, re_path
from . import views

app_name = 'storefront'

urlpatterns = [
    path('detail/<int:product_pk>/', views.product_detail, name='product_detail'),
    re_path(r'$', views.index, name='product_all'),
]
