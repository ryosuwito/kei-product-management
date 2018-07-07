from django.urls import path
from . import views

app_name = 'wilayah'

urlpatterns = [
    path('kota/<str:provinsi>/', views.get_kota, name='kota'),
    path('kecamatan/<str:kota>/', views.get_kecamatan, name='kecamatan'),
    path('kelurahan/<str:kecamatan>/', views.get_kelurahan, name='kelurahan'),
]