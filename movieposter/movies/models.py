from django.db import models
from django.conf import settings


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Movie.Status.PUBLISHED)


class Movie(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликован'

    original_title = models.CharField(
        max_length=100, verbose_name='Оригинальное название')
    adapted_title = models.ForeignKey(
        'AdaptedTitle', on_delete=models.PROTECT, null=True,
        related_name='adapted_title', verbose_name='Адаптированное название'
    )
    description = models.TextField(
        blank=True, max_length=255, verbose_name='Описание')
    poster = models.ImageField(
        upload_to='posters/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Постер')
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, null=True, verbose_name='Категории')
    directors = models.ManyToManyField('Director', through='MovieDirector')
    countries = models.ManyToManyField('Country', verbose_name='Страны')
    tags = models.ManyToManyField(
        'MovieTag', blank=True, related_name='tags', verbose_name='Теги')
    time_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(
        auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name='Статус')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Пользователь')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return (f'{self.original_title}')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-time_created', 'original_title']
        indexes = [
            models.Index(fields=['-time_created']),
        ]


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    def __str__(self):
        return (f'{self.first_name} {self.second_name} {self.date_of_birth}')


class MovieDirector(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.PROTECT)
    director = models.ForeignKey('Director', on_delete=models.PROTECT)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=100)

    def __str__(self):
        return (f'{self.movie} {self.director}')

    class Meta:
        unique_together = ('movie', 'director')


LANGUAGE_CHOICES = [
    ('en', 'Английский'),
    ('ru', 'Русский'),
    ('de', 'Немский'),
    ('fr', 'Французский'),
]


class AdaptedTitle(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    # language = models.CharField(max_length=100, verbose_name='Язык')
    language = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, default='ru',
        verbose_name='Язык'
    )

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'Адаптированное название'
        verbose_name_plural = 'Адаптированные названия'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']


class MovieTag(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    def __str__(self):
        return (f'{self.tag}')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['tag']
