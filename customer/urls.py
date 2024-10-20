from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'customer'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Define more URL patterns as needed
]


