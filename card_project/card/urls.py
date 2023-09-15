from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CardViewSet

router = DefaultRouter()
router.register(r'card', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cards/<uuid:pk>/', CardViewSet.as_view({'patch': 'partial_update'}), name='card-partial-update'),
]