from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Admin
from django.contrib.auth.hashers import make_password

from .models import User, Admin
# Register your models here.

admin.site.register(User)


class BasicUserAdmin(admin.ModelAdmin):
    model = Admin
    list_display = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Admin, BasicUserAdmin)