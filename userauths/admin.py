from django.contrib import admin
from userauths.models import User, Subscribers, CustomerUserRole,FinanceUserRole, StockUserRole, VendorUser

class AdminUsers(admin.ModelAdmin):
    list_display=['username', 'email', 'bio']

# Register your models here.

admin.site.register(Subscribers)
admin.site.register(FinanceUserRole)
admin.site.register(StockUserRole)
admin.site.register(CustomerUserRole)


@admin.register(User)
class userAdmin(admin.ModelAdmin):
    list_display=['username', 'email','bio','verified' ]
@admin.register(VendorUser)
class VendorUserAdmin(admin.ModelAdmin):
    list_display=['title','vendor_address','business_email', 'description']
