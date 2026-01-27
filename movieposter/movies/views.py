from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from .models import Movie, Director, Category, MovieTag, Genre
from .serializers import MovieSerializer, DirectorSerializer, CategorySerializer, MovieTagSerializer, GenreSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination, CursorPagination
from django_filters.rest_framework import DjangoFilterBackend


# class MoviesAPIListPagination(PageNumberPagination):
#     page_size = 12
#     page_size_query_param = 'page_size'
#     max_page_size = 100


class MoviesAPIListPagination(CursorPagination):
    page_size = 12
    ordering = '-time_created'


class DirectorsAPIListPagination(CursorPagination):
    page_size = 12
    ordering = '-date_of_birth'


class MoviesViewSet(viewsets.ModelViewSet):
    # queryset = Movies.objects.all()
    queryset = Movie.published.all()
    serializer_class = MovieSerializer
    lookup_field = 'slug'
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    # permission_classes = (IsAdminOrReadOnly, )
    # permission_classes = (AllowAny, )
    # permission_classes = (IsAuthenticated, )
    pagination_class = MoviesAPIListPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['genres', 'tags', 'directors']

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         permission_classes = [IsAuthenticatedOrReadOnly]
    #     elif self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [AllowAny]
    #     return [permission() for permission in permission_classes]


class AllMoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'slug'
    # permission_classes = (IsAuthenticated, )
    pagination_class = MoviesAPIListPagination


class AllDirectorsViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'slug'
    pagination_class = DirectorsAPIListPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]


class AllCategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class AllGenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class AllMovieTagsViewSet(viewsets.ModelViewSet):
    queryset = MovieTag.objects.all()
    serializer_class = MovieTagSerializer
    lookup_field = 'slug'
