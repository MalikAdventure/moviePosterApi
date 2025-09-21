from rest_framework import serializers
from .models import Movie


class MoviesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movie
        # fields = ('title', 'original_title', 'description', 'poster',
        #           'category', 'countries', 'tags', 'is_published', 'user', 'slug')
        fields = '__all__'
