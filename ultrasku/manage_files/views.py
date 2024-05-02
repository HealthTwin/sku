import csv

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
import pandas as pd

from manage_files.models import UploadedFiles
from manage_files.utils import *
from django.contrib import messages


def uplaod_files(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            read = -1
            file = UploadedFiles.objects.create(
                user_id=request.user.id,
                type_main='noon',
                state_file='بدأ التحميل',
                stat_message='تم بدأ التحميل'
            )
            global file_object
            file_object = {
                "id": file.id,
                "type_main": 'noon',
                "state_file": 'بدأ التحميل',
                "stat_message": 'تم بدأ التحميل',
                "type_file": "",
                "date_upload": file.date_upload
            }
            file_obj = request.FILES.get('file')
            if file_obj.name.endswith('.csv'):
                if file_obj.name.endswith('.csv'):
                    data_frame = pd.read_csv(file_obj)
                    first_row = data_frame.iloc[0]
                    # if 'entered_price' in first_row:
                    #     file.type_file = ' اضافة اسعار المنتجات '
                    #     file_object['type_file'] = 'اضافة اسعار المنتجات '
                    #     save_entered_price_csv(data_frame, request.user)
                    #     read = 1
                    if 'barcode' in first_row:
                        file.type_file = 'تقرير المخزون '
                        file_object['type_file'] = 'تقرير المخزون '
                        save_product_store_csv(data_frame, request.user)
                        read = 1
                    elif 'item_nr' in first_row:
                        file.type_file = 'تقرير المبيعات  الشحنات '
                        file_object['type_file'] = 'تقرير المبيعات  الشحنات '
                        save_sales_items_csv(data_frame, request.user)
                        read = 1
                    elif 'recommended_action' in first_row:
                        file.type_file = 'تقرير  حالات المنتجات'
                        file_object['type_file'] = 'تقرير  حالات المنتجات'
                        save_product_status_csv(data_frame, request.user)
                        read = 1
                    elif 'stock_xdock_net' in first_row:
                        file.type_file = 'المنتاجات المعروضة والغير معروضة'
                        file_object['type_file'] = 'المنتاجات المعروضة والغير معروضة'
                        save_product_live_or_not_csv(data_frame, request.user)
                        read = 1
                    elif 'stock_xdock_net' in first_row:
                        file.type_file = 'المنتاجات المعروضة والغير معروضة'
                        file_object['type_file'] = 'المنتاجات المعروضة والغير معروضة'
                        save_product_live_or_not_csv(data_frame, request.user)
                        read = 1
                    else:
                        read = -1
                        file.type_file = 'ملف غير معروف'
                        file.state_file = 'خطأ'
                        file.stat_message = 'البيانات غير صحيحة'
                        file_object['type_file'] = 'ملق غير معروف'
                        file_object['state_file'] = 'خطأ'
                        file_object['stat_message'] = 'البيانات غير صحيحة'
                        file.save()
            elif file_obj.name.endswith(('.xls', '.xlsx')):
                try:
                    df = pd.read_excel(file_obj)
                    first_object = df.iloc[0]

                    for column_name, cell_value in first_object.items():
                        # if column_name == 'entered_price':
                        #     file.type_file = ' اضافة اسعار المنتجات '
                        #     file_object['type_file'] = 'اضافة اسعار المنتجات '
                        #     save_entered_price_excel(df, request.user)
                        #     read = 1
                        #     break
                        if column_name == "barcode":
                            file.type_file = 'تقرير المخزون '
                            file_object['type_file'] = 'تقرير المخزون '
                            save_product_store_excel(df, request.user)
                            read = 1
                            break
                        elif column_name == "item_nr":
                            file.type_file = 'تقرير المبيعات  الشحنات '

                            file_object['type_file'] = 'تقرير المبيعات  الشحنات '
                            save_sales_items_excel(df, request.user)
                            read = 1
                            break
                        elif column_name == 'recommended_action':
                            file.type_file = 'تقرير  حالات المنتجات'
                            file_object['type_file'] = 'تقرير  حالات المنتجات'
                            save_product_status_excel(df, request.user)
                            read = 1
                            break
                        elif column_name == 'stock_xdock_net':
                            file_object['type_file'] = 'المنتاجات المعروضة والغير معروضة'
                            file.type_file = 'المنتاجات المعروضة والغير معروضة'
                            save_product_live_or_not_excel(df, request.user)
                            read = 1
                            break
                        else:
                            pass

                except Exception as e:
                    file_object['stat_message'] = str(e)
                    file.state_file = 'خطأ',
                    file.stat_message = str(e)
                    read=-1

            if read==0:
                file.state_file = 'توقف التحميل'
                file.type_file = 'ملق غير معروف'
                file.stat_message = 'البيانات غير صحيحة'
                file_object['type_file'] = 'ملق غير معروف'
                file_object['state_file'] = 'خطأ'
                file_object['stat_message'] = 'البيانات غير صحيحة'
            elif read==1:
                file.state_file = 'انتهاء  التحميل',
                file.stat_message = 'تم الانتهاء من التحميل'
                file_object['state_file'] = 'انتهاء  التحميل'
                file_object['stat_message'] = 'تم الانتهاء من التحميل'
            file.save()
        return JsonResponse({}, safe=False)
    else:
        return redirect('/')


def get_status_file(request):
    if request.user.is_authenticated:
        return JsonResponse({'result': file_object})
    else:
        return redirect('/')


def extract_file(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        fields = SalesItems._meta.get_fields()
        column_sales = []
        for field in fields:
            if field.name != 'user':
                column_name = field.name
                data_type = field.get_internal_type()
                column_sales.append((column_name, data_type))
        fields = ProductsStore._meta.get_fields()
        column_products = []
        for field in fields:
            if field.name != 'user':
                column_name = field.name
                data_type = field.get_internal_type()
                column_products.append((column_name, data_type))
        fields = ProductStatus._meta.get_fields()
        column_products_status = []
        for field in fields:
            if field.name != 'user':
                column_name = field.name
                data_type = field.get_internal_type()
                column_products_status.append((column_name, data_type))
        fields = ProductLiveNotLibe._meta.get_fields()
        column_products_live_not = []
        for field in fields:
            if field.name != 'user':
                column_name = field.name
                data_type = field.get_internal_type()
                column_products_live_not.append((column_name, data_type))
        return render(request, 'home/extract.html',
                      context={'title': 'التصدير', 'column_sales': column_sales, 'column_products': column_products,
                               'column_products_status': column_products_status,
                               'column_products_live_not': column_products_live_not})
    else:
        return redirect('')


def extract_products(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        post_data = request.POST

        filters = {}

        for field in ['id', 'qty', 'saleable', 'live_saleable', 'not_live_saleable', 'close_date']:
            if len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and post_data.getlist(field)[1]:
                filters[f'{field}__range'] = (post_data.getlist(field)[0], post_data.getlist(field)[1])
            elif len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and not post_data.getlist(field)[1]:
                filters[field] = post_data.getlist(field)[0]

        for field in ['barcode', 'pbarcode', 'product_title', 'sku', 'partner_sku', 'brand', 'family', 'wh',
                      'country_code']:
            if post_data.get(field):
                filters[f'{field}__icontains'] = post_data.get(field)

        for field in ['non_saleable', 'non_saleable_mislabel', 'non_saleable_expired', 'non_saleable_damaged',
                      'non_saleable_others']:
            if post_data.get(field):
                filters[field] = True

        filters = {k: v for k, v in filters.items() if v}

        filtered_items = ProductsStore.objects.filter(**filters)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        keys_without_csrf = [key for key in request.POST.keys() if key != 'csrfmiddlewaretoken']
        writer.writerow(keys_without_csrf)  # Replace with your actual field names

        # Write the data rows to the CSV file
        for item in filtered_items:
            writer.writerow([getattr(item, field) for field in keys_without_csrf])

        return response
    else:
        return redirect('/')


def extract_sales(request):
    if request.user.is_authenticated:
        post_data = request.POST
        filters = {}

        for field in ['id', 'ordered_date', 'shipped_date', 'delivered_date', 'returned_date', 'return_ndr_due_date',
                      'return_cir_due_date',
                      'base_price', 'seller_price', 'noon_markup', 'offer_price', 'promo_coupon', 'invoice_price',
                      'fee_commission', 'fee_noon_promo', 'fee_noon_markup', 'fee_damaged_return',
                      'fee_outbound_fbn_v2',
                      'payment_due', 'payment_statement_total', 'payment_pending', '']:
            if len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and post_data.getlist(field)[1]:
                filters[f'{field}__range'] = (post_data.getlist(field)[0], post_data.getlist(field)[1])
            elif len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and not post_data.getlist(field)[1]:
                filters[field] = post_data.getlist(field)[0]

        for field in ['item_nr', 'partner_sku', 'sku_config', 'sku', 'family', 'product_type', 'brand', 'product_title',
                      'partner_barcodes', 'city_from', 'city_to', 'country_code', 'item_status', 'commission_type',
                      'sla_type',
                      'currency_code', 'invoice_nr', 'creditnote_nr', 'statement_nrs']:
            if post_data.get(field):
                filters[f'{field}__icontains'] = post_data.get(field)

        for field in ['fx_rate_payment', 'fee_outbound_directship', 'fee_outbound_fbn', 'fee_weight_handling',
                      'fee_reinvoicing', 'fee_crossdock', 'fee_direct_collection', 'fee_noon_penalty',
                      'fee_vat_deducted_at_source', 'fee_crossborder_vat', 'fee_adjustments', 'fee_closing',
                      'indirect_vat', 'promo_deal', 'seller_promo', 'is_fbn']:
            if post_data.get(field):
                filters[field] = True

        filters = {k: v for k, v in filters.items() if v}

        filtered_items = SalesItems.objects.filter(**filters)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales.csv"'

        writer = csv.writer(response)
        keys_without_csrf = [key for key in request.POST.keys() if key != 'csrfmiddlewaretoken']
        writer.writerow(keys_without_csrf)  # Replace with your actual field names

        # Write the data rows to the CSV file
        for item in filtered_items:
            writer.writerow([getattr(item, field) for field in keys_without_csrf])

        return response
    else:
        return redirect('/')


def extract_live_not(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        post_data = request.POST
        filters = {}

        for field in ['id', 'id_partner', 'active_price', 'msrp', 'price', 'sale_price', 'noon_price_min',
                      'noon_price_max',
                      'seller_price_min', 'seller_price_max', 'price_engine_min', 'price_engine_max', 'sale_start_date',
                      'sale_end_date', 'stock_fbn_net']:
            if len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and post_data.getlist(field)[1]:
                filters[f'{field}__range'] = (post_data.getlist(field)[0], post_data.getlist(field)[1])
            elif len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and not post_data.getlist(field)[1]:
                filters[field] = post_data.getlist(field)[0]

        for field in ['noon_status', 'offer_status_reason', 'mp_code', 'stock_xdock_net', 'stock_xdock_gross',
                      'warranty', 'noon_brand', 'noon_title',
                      'sku_child', 'partner_barcodes', 'partner_sku', 'country_code', 'psku_code']:
            if post_data.get(field):
                filters[f'{field}__icontains'] = post_data.get(field)

        for field in ['is_active']:
            if post_data.get(field):
                filters[field] = True

        filters = {k: v for k, v in filters.items() if v}

        filtered_items = ProductLiveNotLibe.objects.filter(**filters)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="live_or_not.csv"'

        writer = csv.writer(response)
        keys_without_csrf = [key for key in request.POST.keys() if key != 'csrfmiddlewaretoken']
        writer.writerow(keys_without_csrf)  # Replace with your actual field names

        # Write the data rows to the CSV file
        for item in filtered_items:
            writer.writerow([getattr(item, field) for field in keys_without_csrf])

        return response
    else:
        return redirect('/')


def extract_status_product(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        post_data = request.POST

        filters = {}

        for field in ['id', 'current_price', 'platform_recommended_price', 'current_fbn_stock',
                      'lowest_processing_days', 'lowest_mp_fbn_price',
                      'lowest_mp_b2b_price', 'external_competition_price', 'average_sku_selling_price',
                      'your_visitors_15_days'
                      ]:
            if len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and post_data.getlist(field)[1]:
                filters[f'{field}__range'] = (post_data.getlist(field)[0], post_data.getlist(field)[1])
            elif len(post_data.getlist(field)) == 2 and post_data.getlist(field)[0] and not post_data.getlist(field)[1]:
                filters[field] = post_data.getlist(field)[0]

        for field in ['b2b_processing_days', 'days_of_coverage', 'live_mp', 'recommended_action', 'country_code',
                      'product_title', 'brand', 'product_type',
                      'family', 'sku', 'sku_config', 'partner_sku']:
            if post_data.get(field):
                filters[f'{field}__icontains'] = post_data.get(field)

        for field in ['shipped_units_15_days', 'revenue_shipped_15_days', 'current_b2b_stock']:
            if post_data.get(field):
                filters[field] = True

        filters = {k: v for k, v in filters.items() if v}

        filtered_items = ProductStatus.objects.filter(**filters)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="status_products.csv"'

        writer = csv.writer(response)
        keys_without_csrf = [key for key in request.POST.keys() if key != 'csrfmiddlewaretoken']
        writer.writerow(keys_without_csrf)

        for item in filtered_items:
            writer.writerow([getattr(item, field) for field in keys_without_csrf])

        return response
    else:
        return redirect('/')


def entered_price(request):
    if request.user.is_authenticated:
        if False:
            messages.info(request, 'يجب الاشتراك اولا ')
            return redirect('/')
        if request.method == 'POST':
            for key, value in request.POST.items():
                try:
                    product = ProductLiveNotLibe.objects.filter(id=key, user=request.user).first()
                    product.sale_price = value
                    product.save()
                except Exception:
                    pass
            messages.success(request, "تم التحديث بنجاح")
            return redirect('/')
        else:
            products = ProductLiveNotLibe.objects.filter(user=request.user)
            return render(request, 'home/entered_price.html', context={'products': products,
                                                                       "title": "الادارة المالية",
                                                                       "sub_title": "add_price"})
    else:
        redirect('/')
