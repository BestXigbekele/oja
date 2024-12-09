from django.contrib import admin
from .models import products,Cart,SubCategory,CartItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', )
    filter_horizontal = ('category2',) 


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(products,ProductAdmin)

admin.site.register(SubCategory)