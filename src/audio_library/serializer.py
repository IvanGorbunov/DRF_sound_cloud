from rest_framework import serializers

from .models import Genre, License


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
        )


class LicenseSerializer(BaseSerializer):
    class Meta:
        model = License
        fields = (
            'id',
            'text',
        )


