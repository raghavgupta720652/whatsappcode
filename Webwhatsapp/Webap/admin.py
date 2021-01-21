from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import *
admin.site.unregister(Group)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display=['email','first_name','last_name','is_active','admin_verified']
    search_fields = ('email', 'first_name', 'last_name', )
    exclude = ['groups','user_permissions']
