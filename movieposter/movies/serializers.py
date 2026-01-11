from rest_framework import serializers
from .models import Movie


class MoviesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movie
        # fields = '__all__'
        fields = (
            'id', 'original_title', 'all_titles', 'description', 'poster',
            'category', 'genres', 'directors', 'countries', 'tags',
            'time_created', 'time_updated', 'is_published', 'user', 'slug'
        )
