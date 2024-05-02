from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('password-reset/', reset_password, name='reset-password'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('logout/', logout_out, name='logout'),
    path('payment/',payment,name='payment'),
    path('verify_payment/',verify_payment,name='verify_payment')

]
