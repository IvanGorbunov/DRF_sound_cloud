import os.path

from django.http import FileResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, parsers, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Genre, License, Album, Track, PlayList, Comment
from .serializer import GenreSerializer, LicenseSerializer, AlbumSerializer, CreateAuthorTrackSerializer, \
    AuthorTrackSerializer, CreatePlayListSerializer, PlayListSerializer, CommentAuthorSerializer, CommentSerializer
from ..base.classes import MixedSerializer, Pagination
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file


class GenreView(generics.ListAPIView):
    """
    Список жанров
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """
    Список лицензий
    """
    serializer_class = LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumView(viewsets.ModelViewSet):
    """
    Список альбомов
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    """
    Список публичных альбомов автора
    """
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    """
    CRUD треков
    """
    serializer_class = CreateAuthorTrackSerializer
    serializer_class_by_action = {
        'list': AuthorTrackSerializer
    }
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    """
    CRUD плейлистов
    """
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = CreatePlayListSerializer
    serializer_class_by_action = {
        'list': PlayListSerializer
    }

    def get_queryset(self):
        return PlayList.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class TrackListView(generics.ListAPIView):
    """
    Список всех треков
    """
    queryset = Track.objects.filter(album__private=False, private=False)
    serializer_class = AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'title',
        'user__display_name',
        'album__name',
        'genre__name'
    ]


class AuthorTrackListView(generics.ListAPIView):
    """
    Список всех треков автора
    """
    serializer_class = AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'title',
        'album__name',
        'genre__name'
    ]

    def get_queryset(self):
        return Track.objects.filter(
            user__id=self.kwargs.get('pk'),
            album__private=False,
            private=False
        )


class StreamingFileView(views.APIView):
    """ Воспроизведение трека
    """
    def set_play(self):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_play()
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response['X-Accel-Redirect'] = f'/mp3/{self.track.file.name}'
            return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StreamingFileAuthorView(views.APIView):
    """ Воспроизведение трека автора
    """
    permission_classes = [IsAuthor]

    def get(self, request, pk):
        self.track = get_object_or_404(Track, id=pk, user=request.user)
        if os.path.exists(self.track.file.path):
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response['X-Accel-Redirect'] = f'/mp3/{self.track.file.name}'
            return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DownloadTrackView(views.APIView):
    """
    Скачивание трека
    """

    def set_download(self):
        self.track.download += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_download()
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response['X-Accel-Redirect'] = f'/media/{self.track.file.name}'
            return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentAuthorView(viewsets.ModelViewSet):
    """
    CRUD комментарие автора
    """
    serializer_class = CommentAuthorSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """
    Комментарии к треку
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(track_id=self.kwargs.get('pk'))


