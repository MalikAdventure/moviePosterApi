from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'photo', 'data_birth')

    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            'Дополнительные настройки',
            {
                'fields': ('photo', 'data_birth'),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
