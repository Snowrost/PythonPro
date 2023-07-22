from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ('owner',)

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_card_status(self, value):
        if (self.instance and self.instance.card_status == 'blocked' and value == 'active') or \
                (self.instance and self.instance.card_status == 'blocked' and value == 'new'):
            raise serializers.ValidationError("Inactive cards cannot be activated again.")
        return value