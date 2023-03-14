from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.

class UserModel(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'username']

admin.site.register(User, UserModel)
admin.site.register(Category)
admin.site.register(ContactModel)
admin.site.register(Admin)
admin.site.register(Writer)
admin.site.register(Reader)
admin.site.register(Post)
admin.site.register(Comment)
