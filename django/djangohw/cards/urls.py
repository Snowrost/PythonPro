from django.urls import path
from .views import CardViewTemp, CardCreateTemp #,CardView

urlpatterns = [
    # path('card/', CardView.as_view(http_method_names=["get", "post"]), name='card-create-get'),
    path('cards/', CardViewTemp.as_view(), name='card_list'),
    path('cards/create/', CardCreateTemp.as_view(), name='create_card'),
    path('cards/save/', CardCreateTemp.as_view(), name='save_card'),
]