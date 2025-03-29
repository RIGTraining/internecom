from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = "RIG Ecommerance"
admin.site.site_title = "RIG Admin Portal"
admin.site.index_title = "Welcome to RIG Researcher Portal"

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name','category','sell_price','balance_qty')
admin.site.register(Items,ItemsAdmin)


admin.site.register(Category)
admin.site.register(subCategory)
admin.site.register(DeliverySystem)
# admin.site.register(Items)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(ItmColor)
admin.site.register(ItmSize)
admin.site.register(ItemOrder)
admin.site.register(Wishlist)







