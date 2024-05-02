
from django.urls import path
from  .views import *

urlpatterns = [
    path('',index,name="index"),
    path('contact/',contact,name="contact"),
    path('why-me/',why_me,name="why_me"),
    path('pricing/',pricing,name='pricing')
]
