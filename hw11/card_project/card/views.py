from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Card
from .serializers import CardSerializer

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

