from rest_framework import viewsets

from packages.models import Letter, Package
from .serializers import LetterSerializer, PackageSerializer


class LetterViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки всех типов запросов с письмами"""
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer


class PackageViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки всех типов запросов с посылками"""
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
