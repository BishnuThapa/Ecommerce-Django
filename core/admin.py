from django.contrib import admin
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
# Register your models here.


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ('user', 'title', 'product_image',
                    'price', 'featured', 'product_status')


admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(ProductImages)
admin.site.register(ProductReview)
admin.site.register(CartOrder)
admin.site.register(CartOrderItems)
admin.site.register(Wishlist)
admin.site.register(Address)
