from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'photo_image', 'data_birth')
    readonly_fields = ['photo_image']

    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            'Дополнительные настройки',
            {
                'fields': ('photo', 'photo_image', 'data_birth'),
            },
        ),
    )

    @admin.display(description='Изображение пользователя')
    def photo_image(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return 'Нет изображения'


admin.site.register(User, CustomUserAdmin)
