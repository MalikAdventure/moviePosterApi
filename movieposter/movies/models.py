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
    description = models.TextField(
        blank=True, max_length=2000, verbose_name='Описание')
    poster = models.ImageField(
        upload_to='posters/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Постер')
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, null=True, verbose_name='Категории')
    genres = models.ManyToManyField('Genre', verbose_name='Жанры')
    directors = models.ManyToManyField('Director', through='MovieDirector')
    countries = models.ManyToManyField('Country', verbose_name='Страны')
    release_date = models.DateField(verbose_name='Дата выхода')
    age_limit = models.PositiveSmallIntegerField(
        verbose_name='Возрастная категория')
    tags = models.ManyToManyField(
        'MovieTag', blank=True, related_name='tags', verbose_name='Теги')
    time_created = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(
        auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name='Статус')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
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
            models.Index(fields=['original_title']),
        ]


class Director(models.Model):
    second_name = models.CharField(
        max_length=100, verbose_name='Фамилия режиссера')
    first_name = models.CharField(max_length=100, verbose_name='Имя режиссера')
    patronymic = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Отчество режиссера')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    objects = models.Manager()

    def __str__(self):
        return (f'{self.first_name} {self.second_name} {self.date_of_birth}')

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'
        ordering = ['second_name', 'first_name', 'patronymic']


class MovieDirector(models.Model):
    movie = models.ForeignKey(
        'Movie', on_delete=models.CASCADE, verbose_name='Название фильма')
    director = models.ForeignKey(
        'Director', on_delete=models.CASCADE, verbose_name='Режиссер')
    date_joined = models.DateField(verbose_name='Дата присоединения к проекту')

    def __str__(self):
        return (f'{self.movie} {self.director}')

    class Meta:
        verbose_name = 'Режиссер-Фильм'
        verbose_name_plural = 'Режиссеры-Фильмы'
        ordering = ['movie', 'director']
        unique_together = ('movie', 'director')


class Category(models.Model):
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    objects = models.Manager()

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name='Название жанра')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    objects = models.Manager()

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name='Название страны')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']


class MovieTag(models.Model):
    tag = models.CharField(max_length=100, db_index=True,
                           verbose_name='Название тега')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    objects = models.Manager()

    def __str__(self):
        return (f'{self.tag}')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['tag']


class AllTitle(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    country = models.ForeignKey(
        'Country', on_delete=models.PROTECT, verbose_name='Страна'
    )
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE,
                              related_name='all_titles', verbose_name='Фильм', null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.country})'

    class Meta:
        verbose_name = 'Адаптированное название'
        verbose_name_plural = 'Адаптированные названия'
        ordering = ['name']
        unique_together = ('country', 'movie')
