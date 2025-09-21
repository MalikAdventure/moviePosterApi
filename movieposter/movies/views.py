from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Movie
from .serializers import MoviesSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination


class MoviesAPIListPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10


class MoviesViewSet(viewsets.ModelViewSet):
    # queryset = Movies.objects.all()
    queryset = Movie.published.all()
    serializer_class = MoviesSerializer
    lookup_field = 'slug'
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    # permission_classes = (IsAdminOrReadOnly, )
    # permission_classes = (AllowAny, )
    permission_classes = (IsAuthenticated, )
    pagination_class = MoviesAPIListPagination

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
    permission_classes = (IsAuthenticated, )
    # pagination_class = MoviesAPIListPagination
