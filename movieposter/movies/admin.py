from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import *


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_title', 'adapted_title', 'poster_image', 'short_description',
                    'category', 'time_created', 'time_updated', 'is_published', 'slug')
    fields = ('original_title', 'slug', 'adapted_title', 'description', 'poster', 'poster_image',
              'category', 'countries', 'tags', 'is_published', 'user')
    readonly_fields = ['poster_image']
    filter_horizontal = ['tags']
    filter_vertical = ['countries']
    list_display_links = ('id', 'original_title')
    search_fields = ('original_title', 'adapted_title__name', 'description')
    list_editable = ('is_published',)
    list_filter = ('category', 'time_created', 'time_updated', 'is_published')
    prepopulated_fields = {'slug': ('original_title',)}
    actions = ['set_published', 'set_draft']
    save_on_top = True
    list_per_page = 12

    @admin.display(description='Изображение постера')
    def poster_image(self, obj):
        if obj.poster:
            return mark_safe(f'<img src="{obj.poster.url}" width="50">')
        return 'Нет изображения'

    @admin.display(description='Краткое описание', ordering='description')
    def short_description(self, obj):
        return f'{obj.description[:20]}'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Movie.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Movie.Status.DRAFT)
        self.message_user(
            request, f'Снято с публикации {count} записей', messages.WARNING)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class MovieTagAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name')
    # list_display_links = ('id', 'name')
    # search_fields = ('name',)
    prepopulated_fields = {'slug': ('tag',)}


admin.site.register(Movie, MovieAdmin)
admin.site.register(AdaptedTitle)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country)
admin.site.register(MovieTag, MovieTagAdmin)
