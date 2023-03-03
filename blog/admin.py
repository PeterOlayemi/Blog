from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.

class UserModel(UserAdmin):
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ('is_writer', 'is_reader', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'age', 'state', 'address', 'picture')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(User, UserModel)
admin.site.register(Category)
admin.site.register(ContactModel)
admin.site.register(Admin)
admin.site.register(Writer)
admin.site.register(Reader)
admin.site.register(Post)
admin.site.register(Comment)