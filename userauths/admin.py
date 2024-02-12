from django.contrib import admin
from userauths.models import User, Subscribers

class AdminUsers(admin.ModelAdmin):
    list_display=['username', 'email', 'bio']

# Register your models here.
admin.site.register(User, AdminUsers)
admin.site.register(Subscribers)