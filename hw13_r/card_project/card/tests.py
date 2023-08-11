from django.test import TestCase
from django.contrib.auth.models import User
from .models import Card
from .tasks import activate_card_task, freeze_expired_cards
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone

class CardActivationTaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.card = Card.objects.create(
            card_name='Test Card',
            card_number='1111222233334444',
            expiry_date='2025-12-31',
            cvv_code='123',
            issue_date='2022-01-01',
            owner=self.user,
            card_status='new',
            card_frig='unfrozen'
        )
        # Create an expired and an active card
        self.expired_card = Card.objects.create(
            card_name='Expired Card',
            card_number='1111222233334444',
            expiry_date=timezone.now() - timezone.timedelta(days=1),
            cvv_code='123',
            issue_date='2022-01-01',
            owner=self.user,
            card_status='active',
            card_frig = 'unfrozen'
        )
        self.active_card = Card.objects.create(
            card_name='Active Card',
            card_number='5555666677778888',
            expiry_date=timezone.now() + timezone.timedelta(days=1),
            cvv_code='456',
            issue_date='2022-01-01',
            owner=self.user,
            card_status='active',
            card_frig = 'unfrozen'
        )



    def test_activate_card_task(self):
        activate_card_task(self.card.id)
        updated_card = Card.objects.get(id=self.card.id)
        self.assertEqual(updated_card.card_status, 'active')

    def test_activate_card(self):
        url = reverse('card-activate', args=[self.card1.id])

        # Unauthorized request (without authentication)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # User authenticated, card belongs to the user, card is inactive
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Card activation process has been initiated.')

        # Card is already active
        url_active_card = reverse('card-activate', args=[self.active_card.id])
        response_active_card = self.client.post(url_active_card)
        self.assertEqual(response_active_card.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_active_card.data['detail'], 'Card is already active.')

        # Card belongs to another user
        self.client.force_authenticate(user=self.another_user)
        response_another_user = self.client.post(url)
        self.assertEqual(response_another_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_freeze_expired_cards(self):
        freeze_expired_cards()

        # Refresh card instances from the database
        self.expired_card.refresh_from_db()
        self.active_card.refresh_from_db()

        # Check if the expired card is frozen (status changed to inactive)
        self.assertEqual(self.expired_card.card_frig, 'frozen')

        # Check if the active card remains unchanged
        self.assertEqual(self.active_card.card_frig, 'unfrozen')
