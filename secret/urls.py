from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import index, SecretViewSet, SecretPassphraseDetailView, SecretKeyDetailView
from .apps import SecretConfig

app_name = SecretConfig.name
router = DefaultRouter()
router.register('generate', SecretViewSet, basename='secret-viewset')

urlpatterns = [
    path('', index, name='index'),
    path('', include(router.urls)),
    path('secrets/<str:passphrase>/', SecretPassphraseDetailView.as_view(), name='secret-detail-view'),
    path('secrets/secret-key/<str:generated_key>/', SecretKeyDetailView.as_view(), name='secret-detail-view')
]
