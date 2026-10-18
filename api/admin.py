from django.contrib import admin
from .models import User, Product


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('IdUser', 'UserName', 'Token')
    search_fields = ('UserName',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)