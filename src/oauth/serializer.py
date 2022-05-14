from rest_framework import serializers

from .models import AuthUser, SocialLink


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
            'avatar',
            'country',
            'city',
            'bio',
            'display_name',
        )


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = (
            'id',
            'link',
        )


class AuthorSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = AuthUser
        fields = (
            'id',
            'avatar',
            'country',
            'city',
            'bio',
            'display_name',
            'social_links',
        )


class GoogleAuth(serializers.Serializer):
    """
    Сериализация данных от Google
    """
    email = serializers.EmailField()
    token = serializers.CharField()
