from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Card


class CardAPITestCase(APITestCase):

    #given
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create some test cards for the user
        self.card1 = Card.objects.create(
            card_name='Card 1',
            card_number='1111222233334444',
            expiry_date='2025-12-31',
            cvv_code='123',
            issue_date='2022-01-01',
            owner=self.user,
            card_status='active',
            card_frig = 'unfrozen'
        )

        self.card2 = Card.objects.create(
            card_name='Card 2',
            card_number='5555666677778888',
            expiry_date='2023-06-30',
            cvv_code='456',
            issue_date='2021-07-01',
            owner=self.user,
            card_status='new',
            card_frig = 'unfrozen'
        )

    def test_list_all_cards(self):
        # given
        url = reverse('card-list')
        # when
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming there are two cards for the user

    def test_retrieve_card_by_id(self):
        # given
        url = reverse('card-detail', args=[self.card1.id])
        # when
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.card1.id))

    def test_create_new_card(self):

        # given
        url = reverse('card-list')
        data = {
            "card_name": "New Card",
            "card_number": "9999888877776666",
            "expiry_date": "2024-05-31",
            "cvv_code": "789",
            "issue_date": "2023-01-01",
            "card_status": "active",
            "card_frig": 'unfrozen'
        }
        # when
        response = self.client.post(url, data)
        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 3)  # Assuming there are three cards after creation

    def test_update_card(self):
        # given
        url = reverse('card-detail', args=[self.card1.id])
        data = {
            "card_name": "Updated Card Name",
            "card_number": "1111222233334444",
            "cvv_code": "999",
            "card_frig": "frozen"
        }
        # when
        response = self.client.patch(url, data)
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the card has been updated correctly
        updated_card = Card.objects.get(id=self.card1.id)
        self.assertEqual(updated_card.card_name, "Updated Card Name")
        self.assertEqual(updated_card.card_number, "1111222233334444")
        self.assertEqual(updated_card.cvv_code, "999")
        self.assertEqual(updated_card.card_frig, "frozen")

