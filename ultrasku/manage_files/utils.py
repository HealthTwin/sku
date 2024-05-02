import math
from datetime import datetime
from manage_files.models import ProductsStore, SalesItems, ProductStatus, ProductLiveNotLibe
from psycopg2 import IntegrityError
from decimal import Decimal
import requests
import re

file_object = {}


def save_product_store_csv(data_frame, user):
    for index, row in data_frame.iterrows():
        product_title = row['product_title']
        brand = row['brand']
        family = row['family']
        close_date = datetime.strptime(row['close_date'], "%Y-%m-%d").date()
        defaults = {
            'pbarcode': row['pbarcode'],
            'barcode': row['barcode'],
            'sku': row['sku'],
            'partner_sku': row['partner_sku'],
            'wh': row['wh'],
            'country_code': row['country_code'],
            'qty': int(row['qty']),
            'saleable': int(row['saleable']),
            'live_saleable': int(row['live_saleable']),
            'not_live_saleable': int(row['not_live_saleable']),
            'non_saleable': bool(row['non_saleable']),
            'non_saleable_damaged': bool(row['non_saleable_damaged']),
            'non_saleable_expired': bool(row['non_saleable_expired']),
            'non_saleable_mislabel': bool(row['non_saleable_mislabel']),
            'non_saleable_others': bool(row['non_saleable_others']),
            'close_date': close_date,
        }
        try:
            product, created = ProductsStore.objects.update_or_create(
                user=user, brand=brand, family=family, product_title=product_title, defaults=defaults
            )
            if not created:
                print(f"Updated data for product_title: {product_title}")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for product_title: {product_title}")


def save_product_store_excel(df, user):
    for index, row in df.iterrows():
        product_title = row['product_title']
        brand = row['brand']
        family = row['family']
        close_date = datetime.strptime(row['close_date'], "%Y-%m-%d").date()
        defaults = {

            'pbarcode': row['pbarcode'],
            'barcode': row['barcode'],
            'sku': row['sku'],
            'partner_sku': row['partner_sku'],

            'wh': row['wh'],
            'country_code': row['country_code'],
            'qty': int(row['qty']),
            'saleable': int(row['saleable']),
            'live_saleable': int(row['live_saleable']),
            'not_live_saleable': int(row['not_live_saleable']),
            'non_saleable': bool(row['non_saleable']),
            'non_saleable_damaged': bool(row['non_saleable_damaged']),
            'non_saleable_expired': bool(row['non_saleable_expired']),
            'non_saleable_mislabel': bool(row['non_saleable_mislabel']),
            'non_saleable_others': bool(row['non_saleable_others']),
            'close_date': close_date,
        }

        try:
            product, created = ProductsStore.objects.update_or_create(
                user=user, brand=brand, family=family, product_title=product_title, defaults=defaults
            )
            if not created:
                print(f"Updated data for product_title: {product_title}")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for product_title: {product_title}")


def save_sales_items_csv(data_frame, user):
    for index, row in data_frame.iterrows():
        item_nr = row['item_nr']
        returned_date = None
        ordered_date = None
        return_ndr_due_date = None
        return_cir_due_date = None
        delivered_date = None
        shipped_date = None
        try:
            returned_date = datetime.strptime(row(['returned_date']), "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            ordered_date = datetime.strptime(row['ordered_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            return_ndr_due_date = datetime.strptime(row['return_ndr_due_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            return_cir_due_date = datetime.strptime(row['return_cir_due_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            delivered_date = datetime.strptime(row['delivered_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            shipped_date = datetime.strptime(row['shipped_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        defaults = {
            'user': user,
            'partner_sku': row['partner_sku'] if 'partner_sku' in row else None,
            'sku_config': row['sku_config'] if 'sku_config' in row else None,
            'sku': row['sku'] if 'sku' in row else None,
            'family': row['family'],
            'product_type': row['product_type'],
            'brand': row['brand'],
            'product_title': row['product_title'],
            'partner_barcodes': row['partner_barcodes'] if 'partner_barcodes' in row else None,
            'city_from': row['city_from'] if 'city_from' in row else None,
            'city_to': row['city_to'] if 'city_to' in row else None,
            'country_code': row['country_code'],
            'item_status': row['item_status'],
            'is_fbn': bool(row['is_fbn']) if 'is_fbn' in row else False,
            'commission_type': row['commission_type'] if 'commission_type' in row else None,
            'sla_type': row['sla_type'] if 'sla_type' in row else None,
            'ordered_date': ordered_date,
            'shipped_date': shipped_date,
            'delivered_date': delivered_date,
            'return_ndr_due_date': return_ndr_due_date,
            'return_cir_due_date': return_cir_due_date,
            'currency_code': row['currency_code'],
            'base_price': Decimal(row['base_price']),
            'seller_promo': bool(row['seller_promo']),
            'seller_price': Decimal(row['seller_price']),
            'noon_markup': Decimal(row['noon_markup']),
            'promo_deal': bool(row['promo_deal']),
            'offer_price': Decimal(row['offer_price']),
            'returned_date': returned_date,
            'promo_coupon': Decimal(row['promo_coupon']),
            'indirect_vat': bool(row['indirect_vat']) if 'indirect_vat' in row else None,
            'payment_statement_total': Decimal(
                row['payment_statement_total']) if 'payment_statement_total' in row else None,
            'invoice_price': Decimal(row['invoice_price']),
            'fee_commission': Decimal(row['fee_commission']) if 'fee_commission' in row else None,
            'fee_closing': bool(row['fee_closing']) if 'fee_closing' in row else None,
            'fee_noon_promo': Decimal(row['fee_noon_promo']),
            'fee_noon_markup': Decimal(row['fee_noon_markup']),
            'fee_adjustments': bool(row['fee_adjustments']) if 'fee_adjustments' in row else None,
            'fee_crossborder_vat': bool(row['fee_crossborder_vat']) if 'fee_crossborder_vat' in row else None,
            'fee_vat_deducted_at_source': bool(
                row['fee_vat_deducted_at_source']) if 'fee_vat_deducted_at_source' in row else None,
            'fee_noon_penalty': bool(row['fee_noon_penalty']),
            'fee_direct_collection': bool(row['fee_direct_collection']),
            'fee_crossdock': bool(row['fee_crossdock']),
            'fee_reinvoicing': bool(row['fee_reinvoicing']),
            'fee_damaged_return': Decimal(row['fee_damaged_return']),
            'fee_weight_handling': bool(row['fee_weight_handling']),
            'fee_outbound_fbn': bool(row['fee_outbound_fbn']) if 'fee_outbound_fbn' in row else None,
            'fee_outbound_fbn_v2': Decimal(row['fee_outbound_fbn_v2']),
            'fee_outbound_directship': bool(
                row['fee_outbound_directship']) if 'fee_outbound_directship' in row else None,
            'payment_due': Decimal(row['payment_due']) if 'payment_due' in row else None,
            'payment_pending': Decimal(row['payment_pending']) if 'payment_pending' in row else None,
            'invoice_nr': row['invoice_nr'],
            'creditnote_nr': row['creditnote_nr'],
            'statement_nrs': row['statement_nrs'] if 'statement_nrs' in row else None,
            'fx_rate_payment': bool(row['fx_rate_payment']) if 'fx_rate_payment' in row else None
        }
        try:
            item, created = SalesItems.objects.update_or_create(
                item_nr=item_nr, defaults=defaults
            )
            if not created:
                print(f"Updated data for product_title: {item_nr}")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for product_title: {item_nr}")


def save_sales_items_excel(df, user):
    for index, row in df.iterrows():

        item_nr = row['item_nr']
        returned_date = None
        ordered_date = None
        return_ndr_due_date = None
        return_cir_due_date = None
        delivered_date = None
        shipped_date = None
        try:
            returned_date = datetime.strptime(row(['returned_date']), "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            ordered_date = datetime.strptime(row['ordered_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            return_ndr_due_date = datetime.strptime(row['return_ndr_due_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            return_cir_due_date = datetime.strptime(row['return_cir_due_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            delivered_date = datetime.strptime(row['delivered_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            shipped_date = datetime.strptime(row['shipped_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        defaults = {
            'user': user,
            'partner_sku': row['partner_sku'] if 'partner_sku' in row else None,
            'sku_config': row['sku_config'] if 'sku_config' in row else None,
            'sku': row['sku'] if 'sku' in row else None,
            'family': row['family'],
            'product_type': row['product_type'],
            'brand': row['brand'],
            'product_title': row['product_title'],
            'partner_barcodes': row['partner_barcodes'] if 'partner_barcodes' in row else None,
            'city_from': row['city_from'] if 'city_from' in row else None,
            'city_to': row['city_to'] if 'city_to' in row else None,
            'country_code': row['country_code'],
            'item_status': row['item_status'],
            'is_fbn': bool(row['is_fbn']) if 'is_fbn' in row else False,
            'commission_type': row['commission_type'] if 'commission_type' in row else None,
            'sla_type': row['sla_type'] if 'sla_type' in row else None,
            'ordered_date': ordered_date,
            'shipped_date': shipped_date,
            'delivered_date': delivered_date,
            'return_ndr_due_date': return_ndr_due_date,
            'return_cir_due_date': return_cir_due_date,
            'currency_code': row['currency_code'],
            'base_price': Decimal(row['base_price']),
            'seller_promo': bool(row['seller_promo']),
            'seller_price': Decimal(row['seller_price']),
            'noon_markup': Decimal(row['noon_markup']),
            'promo_deal': bool(row['promo_deal']),
            'offer_price': Decimal(row['offer_price']),
            'returned_date': returned_date,
            'promo_coupon': Decimal(row['promo_coupon']),
            'indirect_vat': bool(row['indirect_vat']) if 'indirect_vat' in row else None,
            'payment_statement_total': Decimal(
                row['payment_statement_total']) if 'payment_statement_total' in row else None,
            'invoice_price': Decimal(row['invoice_price']),
            'fee_commission': Decimal(row['fee_commission']) if 'fee_commission' in row else None,
            'fee_closing': bool(row['fee_closing']) if 'fee_closing' in row else None,
            'fee_noon_promo': Decimal(row['fee_noon_promo']),
            'fee_noon_markup': Decimal(row['fee_noon_markup']),
            'fee_adjustments': bool(row['fee_adjustments']) if 'fee_adjustments' in row else None,
            'fee_crossborder_vat': bool(row['fee_crossborder_vat']) if 'fee_crossborder_vat' in row else None,
            'fee_vat_deducted_at_source': bool(
                row['fee_vat_deducted_at_source']) if 'fee_vat_deducted_at_source' in row else None,
            'fee_noon_penalty': bool(row['fee_noon_penalty']),
            'fee_direct_collection': bool(row['fee_direct_collection']),
            'fee_crossdock': bool(row['fee_crossdock']),
            'fee_reinvoicing': bool(row['fee_reinvoicing']),
            'fee_damaged_return': Decimal(row['fee_damaged_return']),
            'fee_weight_handling': bool(row['fee_weight_handling']),
            'fee_outbound_fbn': bool(row['fee_outbound_fbn']) if 'fee_outbound_fbn' in row else None,
            'fee_outbound_fbn_v2': Decimal(row['fee_outbound_fbn_v2']),
            'fee_outbound_directship': bool(
                row['fee_outbound_directship']) if 'fee_outbound_directship' in row else None,
            'payment_due': Decimal(row['payment_due']) if 'payment_due' in row else None,
            'payment_pending': Decimal(row['payment_pending']) if 'payment_pending' in row else None,
            'invoice_nr': row['invoice_nr'],
            'creditnote_nr': row['creditnote_nr'],
            'statement_nrs': row['statement_nrs'] if 'statement_nrs' in row else None,
            'fx_rate_payment': bool(row['fx_rate_payment']) if 'fx_rate_payment' in row else None
        }
        try:
            item, created = SalesItems.objects.update_or_create(
                item_nr=item_nr, defaults=defaults
            )
            if not created:
                print(f"Updated data for product_title: {item_nr}")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for product_title: {item_nr}")


def save_product_status_csv(data_frame, user):
    for index, row in data_frame.iterrows():
        product_title = row['product_title']
        defaults = {
            'user': user,
            'partner_sku': row['partner_sku'],
            'sku_config': row['sku_config'],
            'sku': row['sku'],
            'family': row['family'],
            'product_type': row['product_type'],
            'brand': row['brand'],
            'country_code': row['country_code'],
            'recommended_action': row['recommended_action'],
            'live_mp': row['live_mp'],
            'current_price': Decimal(row['current_price']) if not math.isnan(Decimal(row['current_price'])) else None,
            'platform_recommended_price': Decimal(row['platform_recommended_price']) if not math.isnan(
                Decimal(row['platform_recommended_price'])) else None,
            'current_fbn_stock': Decimal(row['current_fbn_stock']) if not math.isnan(
                Decimal(row['current_fbn_stock'])) else None,
            'current_b2b_stock': bool(row['current_b2b_stock']),
            'days_of_coverage': row['days_of_coverage'],
            'b2b_processing_days': row['b2b_processing_days'],
            'lowest_processing_days': Decimal(row['lowest_processing_days']) if not math.isnan(
                Decimal(row['lowest_processing_days'])) else None,
            'lowest_mp_fbn_price': Decimal(row['lowest_mp_fbn_price']) if not math.isnan(
                Decimal(row['lowest_mp_fbn_price'])) else None,
            'lowest_mp_b2b_price': Decimal(row['lowest_mp_b2b_price']) if not math.isnan(
                Decimal(row['lowest_mp_b2b_price'])) else None,
            'external_competition_price': Decimal(row['external_competition_price']) if not math.isnan(
                Decimal(row['external_competition_price'])) else None,
            'average_sku_selling_price': Decimal(row['average_sku_selling_price']) if not math.isnan(
                Decimal(row['average_sku_selling_price'])) else None,
            'your_visitors_15_days': Decimal(row['your_visitors_15_days']) if not math.isnan(
                Decimal(row['your_visitors_15_days'])) else None,
            'revenue_shipped_15_days': bool(row['revenue_shipped_15_days']),
            'shipped_units_15_days': bool(row['shipped_units_15_days'])
        }
        try:
            item, created = ProductStatus.objects.update_or_create(
                product_title=product_title, defaults=defaults
            )
            if not created:
                print(f"Updated data for product_title: {product_title}")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for product_title: {product_title}")


def save_product_status_excel(df, user):
    for index, row in df.iterrows():
        product_title = row['product_title']
        defaults = {
            'user': user,
            'partner_sku': row['partner_sku'],
            'sku_config': row['sku_config'],
            'sku': row['sku'],
            'family': row['family'],
            'product_type': row['product_type'],
            'brand': row['brand'],
            'country_code': row['country_code'],
            'recommended_action': row['recommended_action'],
            'live_mp': row['live_mp'],
            'current_price': Decimal(row['current_price']),
            'platform_recommended_price': Decimal(row['platform_recommended_price']),
            'current_fbn_stock': Decimal(row['current_fbn_stock']),
            'current_b2b_stock': bool(row['current_b2b_stock']),
            'days_of_coverage': row['days_of_coverage'],
            'b2b_processing_days': row['b2b_processing_days'],
            'lowest_processing_days': Decimal(row['lowest_processing_days']),
            'lowest_mp_fbn_price': Decimal(row['lowest_mp_fbn_price']),
            'lowest_mp_b2b_price': Decimal(row['lowest_mp_b2b_price']),
            'external_competition_price': Decimal(row['external_competition_price']),
            'average_sku_selling_price': Decimal(row['average_sku_selling_price']),
            'your_visitors_15_days': Decimal(row['your_visitors_15_days']),
            'revenue_shipped_15_days': bool(row['revenue_shipped_15_days']),
            'shipped_units_15_days': bool(row['shipped_units_15_days'])
        }
        try:
            item, created = ProductStatus.objects.update_or_create(
                product_title=product_title, defaults=defaults
            )
            if not created:
                print(f"Updated data for product_title: {product_title}")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for product_title: {product_title}")


def save_product_live_or_not_csv(data_frame, user):
    for index, row in data_frame.iterrows():
        sale_start_date = None
        sale_end_date = None
        noon_title = row['noon_title']
        psku_code = row['psku_code']
        psku_code = row['psku_code'].replace("',)", "")
        psku_code = psku_code.replace("('", "")
        path_image = get_images(row['sku_child'], psku_code)
        try:
            sale_start_date = datetime.strptime(row(['sale_start_date']), "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            sale_end_date = datetime.strptime(row['sale_end_date'], "%Y-%m-%d").date()
        except Exception:
            pass

        defaults = {
            'image_path': path_image,
            'country_code': row['country_code'],
            'id_partner': int(row['id_partner']),
            'partner_sku': row['partner_sku'],
            'partner_barcodes': row['partner_barcodes'],
            'sku_child': row['sku_child'],
            'noon_brand': row['noon_brand'],
            'active_price': Decimal(row['active_price']) if not math.isnan(Decimal(row['active_price'])) else None,
            'msrp': Decimal(row['msrp']) if not math.isnan(Decimal(row['msrp'])) else None,
            'price': Decimal(row['price']) if not math.isnan(Decimal(row['price'])) else None,
            'sale_price': Decimal(row['sale_price']) if not math.isnan(Decimal(row['sale_price'])) else None,
            'noon_price_min': Decimal(row['noon_price_min']) if not math.isnan(
                Decimal(row['noon_price_min'])) else None,
            'noon_price_max': Decimal(row['noon_price_max']) if not math.isnan(
                Decimal(row['noon_price_max'])) else None,
            'seller_price_min': Decimal(row['seller_price_min']) if not math.isnan(
                Decimal(row['seller_price_min'])) else None,
            'seller_price_max': Decimal(row['seller_price_max']) if not math.isnan(
                Decimal(row['seller_price_max'])) else None,
            'price_engine_min': Decimal(row['price_engine_min']) if not math.isnan(
                Decimal(row['price_engine_min'])) else None,
            'price_engine_max': Decimal(row['price_engine_max']) if not math.isnan(
                Decimal(row['price_engine_max'])) else None,
            'sale_start_date': sale_start_date,
            'sale_end_date': sale_end_date,
            'is_active': bool(row['is_active']),
            'warranty': row['warranty'],
            'stock_fbn_net': Decimal(row['stock_fbn_net']) if not math.isnan(Decimal(row['stock_fbn_net'])) else None,
            'mp_code': row['mp_code'],
            'offer_status_reason': row['offer_status_reason'] if 'offer_status_reason' in row else '',
            'noon_status': row['noon_status']
        }
        try:
            item, created = ProductLiveNotLibe.objects.update_or_create(
                user=user, psku_code=psku_code, noon_title=noon_title, defaults=defaults
            )
            if not created:
                print(f"Updated data for noon_title:")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for noon_title")


def save_product_live_or_not_excel(df, user):
    for index, row in df.iterrows():
        sale_start_date = None
        sale_end_date = None
        noon_title = row['noon_title']
        psku_code = row['psku_code'].replace("',)", "")
        psku_code = psku_code.replace("('", "")
        path_image=get_images(row['sku_child'],psku_code)
        try:
            sale_start_date = datetime.strptime(row(['sale_start_date']), "%Y-%m-%d").date()
        except Exception:
            pass
        try:
            sale_end_date = datetime.strptime(row['sale_end_date'], "%Y-%m-%d").date()
        except Exception:
            pass
        defaults = {
            'image_path':path_image,
            'country_code': row['country_code'],
            'id_partner': int(row['id_partner']),
            'partner_sku': row['partner_sku'],
            'partner_barcodes': row['partner_barcodes'],
            'sku_child': row['sku_child'],
            'noon_brand': row['noon_brand'],
            'active_price': Decimal(row['active_price']) if not math.isnan(Decimal(row['active_price'])) else None,
            'msrp': Decimal(row['msrp']) if not math.isnan(Decimal(row['msrp'])) else None,
            'price': Decimal(row['price']) if not math.isnan(Decimal(row['price'])) else None,
            'sale_price': Decimal(row['sale_price']) if not math.isnan(Decimal(row['sale_price'])) else None,
            'noon_price_min': Decimal(row['noon_price_min']) if not math.isnan(
                Decimal(row['noon_price_min'])) else None,
            'noon_price_max': Decimal(row['noon_price_max']) if not math.isnan(
                Decimal(row['noon_price_max'])) else None,
            'seller_price_min': Decimal(row['seller_price_min']) if not math.isnan(
                Decimal(row['seller_price_min'])) else None,
            'seller_price_max': Decimal(row['seller_price_max']) if not math.isnan(
                Decimal(row['seller_price_max'])) else None,
            'price_engine_min': Decimal(row['price_engine_min']) if not math.isnan(
                Decimal(row['price_engine_min'])) else None,
            'price_engine_max': Decimal(row['price_engine_max']) if not math.isnan(
                Decimal(row['price_engine_max'])) else None,
            'sale_start_date': sale_start_date,
            'sale_end_date': sale_end_date,
            'is_active': bool(row['is_active']),
            'warranty': row['warranty'],
            'stock_fbn_net': Decimal(row['stock_fbn_net']) if not math.isnan(Decimal(row['stock_fbn_net'])) else None,
            'mp_code': row['mp_code'],
            'offer_status_reason': row['offer_status_reason'] if 'offer_status_reason' in row else '',
            'noon_status': row['noon_status']
        }
        try:
            item, created = ProductLiveNotLibe.objects.update_or_create(
                user=user, psku_code=psku_code, noon_title=noon_title, defaults=defaults
            )

            if not created:
                print(f"Updated data for noon_title:")
        except IntegrityError:
            print(f"Error occurred while updating/creating data for noon_title:")


def is_decimal(value):
    try:
        Decimal(value)
        return True
    except (TypeError, ValueError):
        return False


#
# def save_entered_price_csv(data_frame, user):
#     for index, row in data_frame.iterrows():
#         try:
#             product = SalesItems.objects.filter(id=row['id'], user=user).first()
#             product.entered_price = Decimal(row['entered_price']) if row['entered_price'] else 0.0
#             product.save()
#         except Exception:
#             pass
#
#
# def save_entered_price_excel(df, user):
#     for index, row in df.iterrows():
#         try:
#             product = SalesItems.objects.filter(id=row['id'], user=user).first()
#             product.entered_price = Decimal(row['entered_price']) if row['entered_price'] else 0.0
#             product.save()
#         except Exception:
#             pass

def get_images(sku, sku_code):
    url = "https://www.noon.com/saudi-en/" + sku + "/p/?o=" + sku_code

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        image_url_pattern = r"https://f\.nooncdn\.com/p/v\d+/.*?\.jpg"
        image_urls = re.findall(image_url_pattern, html_content)

        if image_urls:
            return image_urls[0]
        else:
            return ''
    else:
        return ''
