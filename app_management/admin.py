from django.contrib import admin
from .models import Artist, Album, MetalHead
from django.contrib.auth.admin import UserAdmin


admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(MetalHead, UserAdmin)

