from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Category,Subcategory,Brand,Order])
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','image','name','desc','price','date','category']
    list_display_links=['name','image']
    list_per_page=10
    search_fields=['name']
    list_filter=['price','name']
    ordering=['name']

