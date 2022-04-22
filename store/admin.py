from pyexpat import model
from django.contrib import admin

from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','slug','description','price','category','is_available')
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(Product,ProductAdmin)
