from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Card
from .serializers import CardSerializer
from .tasks import activate_card_task

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PUT' not allowed. Use 'PATCH' for Raw Data."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        card = self.get_object()

        fields_allowed_to_update = ['card_name', 'card_number', 'cvv_code', 'card_frig']
        serializer = self.get_serializer(card, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for field in fields_allowed_to_update:
            setattr(card, field, serializer.validated_data.get(field))

        card.save()
        return Response(serializer.data)

    queryset = Card.objects.none()

    def activate_card(self, request, pk=None):
        card = self.get_object()

        if card.owner != self.request.user:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        if card.card_status == 'new':
            activate_card_task.delay(card.id)
            return Response({"detail": "Card activation process has been initiated."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Card is already active."}, status=status.HTTP_400_BAD_REQUEST)

