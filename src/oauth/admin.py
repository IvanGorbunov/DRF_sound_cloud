from django.contrib import admin
from . import models


@admin.register(models.AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'display_name',
        'join_date',
    )
    list_display_links = (
        'id',
        'email',
    )


@admin.register(models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'link',
    )
    list_display_links = (
        'id',
        'user',
    )


