from django.contrib import admin

from manage_files.models import ProductsStore, SalesItems, ProductLiveNotLibe, ProductStatus

# Register your models here.
admin.site.register(ProductsStore)
admin.site.register(SalesItems)
admin.site.register(ProductLiveNotLibe)
admin.site.register(ProductStatus)