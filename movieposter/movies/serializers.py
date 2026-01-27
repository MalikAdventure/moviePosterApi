from rest_framework import serializers
from .models import Movie, Director, Genre, Country, MovieTag, AllTitle, Category


class DirectorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Director
        fields = '__all__'

    def get_full_name(self, obj):
        parts = [obj.second_name, obj.first_name, obj.patronymic]
        return " ".join([p for p in parts if p])


class AllTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllTitle
        fields = ['id', 'name']


class MovieTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieTag
        fields = ['id', 'tag']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    all_titles = AllTitleSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    directors = DirectorSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    tags = MovieTagSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movie
        fields = (
            'id', 'original_title', 'all_titles', 'description', 'poster',
            'category', 'genres', 'directors', 'countries', 'release_date', 'age_limit', 'tags',
            'time_created', 'time_updated', 'is_published', 'user', 'slug'
        )
