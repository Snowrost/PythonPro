import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Card


class CardViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_card_by_valid_card_number(self):
        # Create a test card
        card = Card.objects.create(
            card_number="2104676720671468",
            expiry_date="12/23",
            cvv_code="123",
            issue_date="2023-01-01",
            owner_id="d4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e",
            card_status="active"
        )

        # Make a GET request to retrieve the card by its valid card number
        url = reverse('card-create-get')
        response = self.client.get(url, {'card_number': card.card_number})

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['card_number'], card.card_number)

    def test_get_card_by_invalid_card_number(self):
        # Make a GET request with an invalid card number
        url = reverse('card-create-get')
        response = self.client.get(url, {'card_number': '3422342342342'})

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Card not found')

    def test_get_card_without_card_number(self):
        # Make a GET request without providing a card number
        url = reverse('card-create-get')
        response = self.client.get(url)

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Please provide a card number.')

    # Create a valid card data
    def _generate_valid_card_data(self):
        return {
            'card_number': '6521938157614486',
            'expiry_date': '12/23',
            'cvv_code': '123',
            'issue_date': '2023-01-01',
            'owner_id': 'd4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e',
            'card_status': 'active'
        }

    def test_create_valid_card(self):
        # Create a valid card data
        card_data = self._generate_valid_card_data()

        # Make a POST request to create a valid card
        url = reverse('card-create-get')
        response = self.client.post(url, data=json.dumps(card_data), content_type='application/json')

        # Assert the response status code and success message
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Card created successfully')

    def test_create_invalid_card(self):
        # Create an invalid card data with an invalid card number
        card_data = self._generate_valid_card_data()
        card_data['card_number'] = '4532015112893798'

        # Make a POST request to create an invalid card
        url = reverse('card-create-get')
        response = self.client.post(url, data=json.dumps(card_data), content_type='application/json')

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid card number.')


class CardModelTest(TestCase):
    def test_is_valid_valid_card_number(self):
        # given
        # Create a card with a valid card number
        card = Card(card_number="6521938157614486")

        # Check the validity of the card number
        is_valid = card.is_valid()

        # Assert the result
        self.assertTrue(is_valid)

    def test_is_valid_invalid_card_number(self):
        # given
        # Create a card with an invalid card number
        card = Card(card_number="1234567890123456")

        # when
        # Check the validity of the card number
        is_valid = card.is_valid()

        # then
        # Assert the result
        self.assertFalse(is_valid)
