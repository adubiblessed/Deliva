from django.contrib import admin

from .models import User


admin.site.site_header = "Deliva Administration"
admin.site.index_title = "Deliva Admin Portal"
admin.site.site_title = "Deliva Admin"


admin.site.register(User)