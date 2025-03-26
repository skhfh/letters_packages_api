from django.urls import include, path
from rest_framework import routers

from .views import LetterViewSet, PackageViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'letters', LetterViewSet, basename='letters')
router.register(r'packages', PackageViewSet, basename='packages')


urlpatterns = [
    path('', include(router.urls)),
]
