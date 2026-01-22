from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Movie, Director
from .serializers import MoviesSerializer, DirectorsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination, CursorPagination
from django_filters.rest_framework import DjangoFilterBackend


# class MoviesAPIListPagination(PageNumberPagination):
#     page_size = 12
#     page_size_query_param = 'page_size'
#     max_page_size = 100


class MoviesAPIListPagination(CursorPagination):
    page_size = 10
    ordering = '-time_created'


class MoviesViewSet(viewsets.ModelViewSet):
    # queryset = Movies.objects.all()
    queryset = Movie.published.all()
    serializer_class = MoviesSerializer
    lookup_field = 'slug'
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    # permission_classes = (IsAdminOrReadOnly, )
    # permission_classes = (AllowAny, )
    # permission_classes = (IsAuthenticated, )
    pagination_class = MoviesAPIListPagination
    filter_backends = [DjangoFilterBackend]
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
    serializer_class = MoviesSerializer
    lookup_field = 'slug'
    # permission_classes = (IsAuthenticated, )
    # pagination_class = MoviesAPIListPagination
    pagination_class = MoviesAPIListPagination


class AllDirectorsViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorsSerializer
    lookup_field = 'slug'
