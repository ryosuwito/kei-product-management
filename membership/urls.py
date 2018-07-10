from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('profile/<int:pk>/', views.profile_page, name='profile'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('choose/', views.pre_register_page, name='pre_register'),
    path('profile/edit', views.edit_profile_page, name='edit_profile'),
    path('profile/', views.profile_page, name='profile'),
]