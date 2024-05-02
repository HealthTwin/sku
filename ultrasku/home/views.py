from django.shortcuts import render, redirect
from django.db.models import Sum, Count, F, Avg, FloatField, DecimalField, Subquery, OuterRef
from django.db.models.functions import ExtractMonth, ExtractYear
from manage_files.models import UploadedFiles, ProductsStore, ProductLiveNotLibe, SalesItems, ProductStatus
from datetime import date, timedelta
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_data = request.user
        tody_base_price = SalesItems.objects.filter(user=request.user, ordered_date=date.today()).aggregate(
            Sum('base_price'))
        yesterday_base_price = SalesItems.objects.filter(user=request.user,
                                                         ordered_date=date.today() - timedelta(days=1)).aggregate(
            Sum('base_price'))
        first_day_of_month = date.today().replace(day=1)

        last_day_of_month = (date.today() + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        this_month = SalesItems.objects.filter(user=request.user,
                                               ordered_date__range=(first_day_of_month, last_day_of_month)).aggregate(
            Sum('base_price'))

        first_day_of_current_month = date.today().replace(day=1)

        last_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
        first_day_of_last_month = last_month.replace(day=1)

        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)

        last_month_price = SalesItems.objects.filter(user=request.user,
                                                     ordered_date__range=(
                                                         first_day_of_last_month, last_day_of_last_month)).aggregate(
            Sum('base_price'))

        related_skus = ProductLiveNotLibe.objects.filter(sku_child=OuterRef('sku'),user=request.user).values('sku_child')

        queryset = SalesItems.objects.filter(sku__in=Subquery(related_skus),user=request.user).annotate(
            id_count=Count('id'),
            total_seller_price=Sum('seller_price'),
            image_path=Subquery(ProductLiveNotLibe.objects.filter(sku_child=OuterRef('sku'),user=request.user).values('image_path')[:1])
        )

        top_items = queryset.values('product_title', 'total_seller_price', 'image_path').annotate(
            id_count=Count('id')).filter(
            id_count__gt=3)
        all_items = queryset.values('product_title', 'total_seller_price', 'image_path').annotate(id_count=Count('id'))

        return render(request, 'home/home.html', context={"title": "home", "user_data": user_data,
                                                          "tody": tody_base_price['base_price__sum'] if tody_base_price[
                                                              'base_price__sum'] else '0',
                                                          "yesterday": yesterday_base_price['base_price__sum'] if
                                                          yesterday_base_price['base_price__sum'] else '0',
                                                          "last_month_price": last_month_price['base_price__sum'] if
                                                          last_month_price['base_price__sum'] else '0'
            , "this_month": this_month['base_price__sum'] if this_month['base_price__sum'] else '0',
                                                          "top_items": top_items,
                                                          "all_items": all_items})
    else:
        return redirect('/')


def insert(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request,'يجب الاشتراك اولا ')
            return redirect('/')
        return render(request, 'home/insert.html', context={"title": "insert", "files": UploadedFiles.objects.filter(
            user_id=request.user).order_by('-id')})
    else:
        return redirect('/')


def all_products(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request,'يجب الاشتراك اولا ')
            return redirect('/')
        products = ProductsStore.objects.filter(user=request.user)
        return render(request, 'home/products.html',
                      context={'title': 'إدارة المنتجات', 'sub_title': 'عام', 'products': products})
    else:
        return redirect('/')


def lives_products(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request,'يجب الاشتراك اولا ')
            return redirect('/')
        products = ProductLiveNotLibe.objects.filter(user=request.user, noon_status='live')
        return render(request, 'home/products_live.html',
                      context={'title': 'إدارة المنتجات', 'sub_title': 'فعال', 'products': products})
    else:
        redirect('/')


def not_lives_products(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request,'يجب الاشتراك اولا ')
            return redirect('/')
        products = ProductLiveNotLibe.objects.filter(user=request.user, noon_status='not_live')
        return render(request, 'home/products_not_live.html',
                      context={'title': 'إدارة المنتجات', 'sub_title': 'الغير فعال', 'products': products})
    else:
        redirect('/')


def sales_products(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request,'يجب الاشتراك اولا ')
            return redirect('/')
        products = SalesItems.objects.filter(user=request.user)
        return render(request, 'home/items_sales.html',
                      context={'title': 'تقارير المبيعات', 'sub_title': 'حسب المنتج', 'products': products})
    else:
        redirect('/')


def report_days(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request,'يجب الاشتراك اولا ')
            return redirect('/')
        sales_items_grouped = SalesItems.objects.filter(item_status='delivered', user=request.user).values(
            'ordered_date').annotate(
            total_base_price=Sum('base_price'),
            total_seller_price=Sum('seller_price'),
            total_invoice_price=Sum('invoice_price')
        ).order_by('ordered_date')
        return render(request, 'home/items_sales_daily.html',
                      context={'title': 'تقارير المبيعات', 'sub_title': 'المبيعات اليومية',
                               'products': sales_items_grouped})
    else:
        redirect('/')


def report_month(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        sales_items_grouped = SalesItems.objects.filter(item_status='delivered', user=request.user).annotate(
            month=ExtractMonth('ordered_date')
        ).values('month').annotate(
            total_base_price=Sum('base_price'),
            total_seller_price=Sum('seller_price'),
            total_invoice_price=Sum('invoice_price')
        ).order_by('month')
        return render(request, 'home/items_sales_month.html',
                      context={'title': 'تقارير المبيعات', 'sub_title': 'حسب الشهر',
                               'products': sales_items_grouped})
    else:
        redirect('/')


def report_year(request):

    if request.user.is_authenticated:
        if False:
            messages.info(request,'يجب الاشتراك اولا ')
            return redirect('/')
        sales_items_grouped = SalesItems.objects.filter(item_status='delivered', user=request.user).annotate(
            year=ExtractYear('ordered_date')
        ).values('year').annotate(
            total_base_price=Sum('base_price'),
            total_seller_price=Sum('seller_price'),
            total_invoice_price=Sum('invoice_price')
        ).order_by('year')
        return render(request, 'home/fbn.html',
                      context={'title': 'تقارير المبيعات', 'sub_title': 'حسب السنة',
                               'products': sales_items_grouped})
    else:
        redirect('/')


def fbn(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        products = SalesItems.objects.filter(user=request.user, is_fbn=True)
        return render(request, 'home/fbn.html',
                      context={'title': 'طلبات FBN', 'products': products})
    else:
        redirect('/')


def get_report_sales(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        sales_data = ProductLiveNotLibe.objects.filter(user=request.user).values('noon_title').annotate(
            total_count=Count('id'),
            avg_seller_price=Avg('price'),
            avg_entered_price=Avg('sale_price'),
            total_seller_price=Sum('price'),
            total_entered_price=Sum('sale_price'),
            total_price_difference=Sum(F('sale_price')) - Sum(F('price'), output_field=DecimalField())
        )

        total_price_difference_sum = sum(
            item['total_price_difference'] for item in sales_data if item['total_price_difference'] is not None)

        return render(request, "home/reports_sales.html", context={'products': sales_data, 'title': 'الادارة المالية',
                                                                   'sub_title': 'الربح',
                                                                  'total_price_difference_sum': total_price_difference_sum, })
    else:
        redirect('/')


def statistics(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        sku = ProductLiveNotLibe.objects.filter(user=request.user).count()
        active = ProductLiveNotLibe.objects.filter(noon_status='live',user=request.user).count()
        not_active = ProductLiveNotLibe.objects.filter(noon_status='not live',user=request.user).count()
        sales = SalesItems.objects.filter(user=request.user).count()
        average_seller_price = SalesItems.objects.filter(user=request.user).aggregate(avg_seller_price=Avg('seller_price'))
        avg_seller_price = average_seller_price['avg_seller_price']
        return render(request, 'home/statistics.html', context={'title': 'statistics', 'sku': sku, 'active': active,
                                                                'not_active': not_active, 'sales': sales,'avg_seller_price':avg_seller_price})
    else:
        redirect('/')

def elmonafseen(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        grouped_results = ProductStatus.objects.filter(user=request.user).values('recommended_action').annotate(
            recommended_action_count=Count('recommended_action'))
        recommended_actions = [result['recommended_action'] for result in grouped_results]
        recommended_action_counts = [result['recommended_action_count'] for result in grouped_results]
        return render(request, 'home/elmonafseen.html',context={'title':'elmonafseen','labels':recommended_actions,
                                                            'data':recommended_action_counts})
    else:
        redirect('/')