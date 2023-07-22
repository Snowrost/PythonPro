from django.contrib.auth.models import User
from django.db import models
import uuid


class Card(models.Model):
    CARD_STATUS = (
        ('new', 'New'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    )

    CARD_REFRIGIRATOR = (
        ('unfrozen', 'Provided',),
        ('frozen', 'Frozen',),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()
    cvv_code = models.CharField(max_length=4)
    issue_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_status = models.CharField(max_length=10, choices=CARD_STATUS, default='new')
    card_frig = models.CharField(max_length=10, choices=CARD_REFRIGIRATOR, default='new')

    def __str__(self):
        return self.card_name

    def status_validate(self, *args, **kwargs):
        if self.pk:
            original_card = Card.objects.get(pk=self.pk)
            if (original_card.card_status == 'blocked' and self.card_status == 'active') or (original_card.card_status == 'blocked' and self.card_status == 'new'):
                raise ValueError("blocked cards cannot be activated again.")
        super().save(*args, **kwargs)