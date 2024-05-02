
from django.urls import path
from  .views import *

urlpatterns = [
    path('',home,name="home"),
    path('insert/',insert,name='insert'),
    path('all_products/',all_products,name="all_products"),
    path('lives_products/',lives_products,name='lives_products'),
    path('not_lives_products/',not_lives_products,name='not_lives_products'),
    path('sales_products/',sales_products,name='sales_products'),
    path('report_days/',report_days,name='report_days'),
    path('report_month/',report_month,name='report_month'),
    path('report_year/',report_year,name='report_year'),
    path('fbn/',fbn,name='fbn'),
    path('get_report_sales/',get_report_sales,name="get_report_sales"),
    path('statistics/',statistics,name='statistics'),
    path('elmonafseen/',elmonafseen,name='elmonafseen')
]
