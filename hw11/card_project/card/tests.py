from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Card
import datetime
from datetime import date

class CardAPITestCase(APITestCase):

    #given
    def setUp(self):
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


        #!TODO Check what data is returned, and whether the card was created correctly in the database.
        self.assertEqual(response.data[0]['card_name'], self.card1.card_name)
        self.assertEqual(response.data[0]['card_number'], '1111222233334444')
        self.assertEqual(response.data[0]['expiry_date'], self.card1.expiry_date)
        self.assertEqual(response.data[0]['cvv_code'], '123')
        self.assertEqual(response.data[0]['issue_date'], '2022-01-01')
        self.assertEqual(response.data[0]['card_status'], 'active')
        self.assertEqual(response.data[0]['card_frig'], 'unfrozen')
        self.assertEqual(response.data[1]['card_name'], self.card2.card_name)

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
        expiry_date = datetime.datetime.strptime(data['expiry_date'], "%Y-%m-%d").date()
        issue_date = datetime.datetime.strptime(data['issue_date'], "%Y-%m-%d").date()
        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #!TODO Check what data is returned, and whether the card was created correctly in the database.
        self.assertEqual(response.data['card_name'], data['card_name'])
        self.assertEqual(response.data['card_number'], data['card_number'])
        self.assertEqual(response.data['cvv_code'], data['cvv_code'])

        # Check if the card has been created correctly in the database
        self.assertEqual(Card.objects.count(), 3)
        new_card = Card.objects.get(id=response.data['id'])
        self.assertEqual(new_card.card_name, data['card_name'])
        self.assertEqual(new_card.card_number, data['card_number'])
        self.assertEqual(new_card.cvv_code, data['cvv_code'])
        self.assertEqual(new_card.expiry_date, expiry_date)
        self.assertEqual(new_card.issue_date,  issue_date)
        self.assertEqual(new_card.card_status, data['card_status'])
        self.assertEqual(new_card.card_frig, data['card_frig'])

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

        #!TODO Check what data is returned, and whether the card was created correctly in the database.
        self.assertEqual(response.data['card_name'], data['card_name'])
        self.assertEqual(response.data['cvv_code'], data['cvv_code'])
        self.assertEqual(response.data['card_frig'], data['card_frig'])

        # Check if the card has been updated correctly
        updated_card = Card.objects.get(id=self.card1.id)
        self.assertEqual(updated_card.card_name, "Updated Card Name")
        self.assertEqual(updated_card.card_number, "1111222233334444")
        self.assertEqual(updated_card.cvv_code, "999")
        self.assertEqual(updated_card.card_frig, "frozen")

