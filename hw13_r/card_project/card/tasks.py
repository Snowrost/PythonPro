from celery import shared_task
from time import sleep
from .models import Card
from django.utils import timezone
@shared_task
def activate_card_task(card_id):
    try:
        card = Card.objects.get(id=card_id)
        if card.card_status == 'new':
            # Simulating a delay of 20 seconds before activating the card
            import time
            time.sleep(20)
            card.card_status = 'active'
            card.save()
    except Card.DoesNotExist:
        pass

@shared_task
def freeze_expired_cards():
    # Freeze cards with expiry date greater than today
    expired_cards = Card.objects.filter(expiry_date__lt=timezone.now(), card_frig='unfrozen')
    expired_cards.update(card_frig='frozen')