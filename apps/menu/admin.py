from django.contrib import admin

# Register your models here.
from .models import MenuItem, MenuCategory

admin.site.register(MenuItem)
admin.site.register(MenuCategory)