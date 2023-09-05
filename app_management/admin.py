from django.contrib import admin
from .models import Artist, Album, Role, Member, AlbumContributor
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Member)

