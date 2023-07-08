from django.urls import path
from .views import CardView

urlpatterns = [
    path('cards/', CardView.as_view(http_method_names=["get", "post"]), name='card-create-get'),
]