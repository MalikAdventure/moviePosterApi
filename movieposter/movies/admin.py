from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import *


class AllTitleInline(admin.TabularInline):
    model = AllTitle
    extra = 1
    fields = ('name', 'country')


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_title', 'get_all_titles', 'poster_image', 'short_description',
                    'category', 'time_created', 'time_updated', 'is_published', 'slug')
    fields = ('original_title', 'slug', 'description', 'poster', 'poster_image',
              'category', 'genres', 'countries', 'tags', 'is_published', 'user')
    inlines = [AllTitleInline]
    readonly_fields = ['poster_image']
    filter_horizontal = ['tags']
    filter_vertical = ['countries']
    list_display_links = ('id', 'original_title')
    search_fields = ('original_title', 'all_title__name', 'description')
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

    @admin.display(description='Адаптированные названия')
    def get_all_titles(self, obj):
        return ', '.join([f'{title.country}: {title.name}' for title in obj.all_titles.all()])


class AllTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'movie')
    list_display_links = ('id', 'name', 'country', 'movie')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class MovieTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tag',)}


class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('second_name', 'first_name', 'patronymic')}


admin.site.register(Movie, MovieAdmin)
admin.site.register(AllTitle, AllTitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(MovieTag, MovieTagAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(MovieDirector)
