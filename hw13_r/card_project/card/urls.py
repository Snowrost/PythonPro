from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CardViewSet

router = DefaultRouter()
router.register(r'card', CardViewSet)

card_list = CardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

card_detail = CardViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
    'post': 'activate_card'  # Add this line
})

urlpatterns = [
    path('', include(router.urls)),
    path('cards/<uuid:pk>/', CardViewSet.as_view({'patch': 'partial_update'}), name='card-partial-update'),
    path('cards/<uuid:pk>/', card_detail, name='card-detail'),
]