from django.contrib import admin
from .models import Category, Supplier, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, WishList, Address

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor_image')



class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 3  # Number of empty forms to show for adding new images


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImagesInline]
    list_display = ('title', 'price', 'quantity_available', 'is_available', 'category', 'product_image','user','featured',  'product_status')


@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'price', 'payment_status', 'order_date', 'order_status')

@admin.register(CartOrderItems)
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'invoice_number', 'item', 'price', 'total', 'qty', 'order_image')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'review', 'ratings', 'date')

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'status')