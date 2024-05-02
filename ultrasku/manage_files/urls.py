"""
URL configuration for ultrasku project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('upload/',uplaod_files,name="upload" ),
    path('get_status_file/',get_status_file,name='get_status_file'),
    path('extract_file/',extract_file,name='extract_file'),
    path('extract_products/',extract_products,name='extract_products'),
    path('extract_sales/',extract_sales,name='extract_sales'),
    path('extract_live_not/',extract_live_not,name='extract_live_not'),
    path('extract_status_product/',extract_status_product,name='extract_status_product'),
    path('entered_price/',entered_price,name="entered_price")
]
