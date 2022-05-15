from rest_framework import generics, viewsets

from .models import Genre, License
from .serializer import GenreSerializer, LicenseSerializer
from ..base.permissions import IsAuthor


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
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

