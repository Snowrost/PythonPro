import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Card



# class CardViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#
#     def test_get_card_by_valid_card_number(self):
#         # Create a test card
#         card = Card.objects.create(
#             card_number="2104676720671468",
#             expiry_date="12/23",
#             cvv_code="123",
#             issue_date="2023-01-01",
#             owner_id="d4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e",
#             card_status="active"
#         )
#
#         # Make a GET request to retrieve the card by its valid card number
#         url = reverse('card-create-get')
#         response = self.client.get(url, {'card_number': card.card_number})
#
#         # Assert the response status code and data
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content)
#         self.assertEqual(data['card_number'], card.card_number)
#
#     def test_get_card_by_invalid_card_number(self):
#         # Make a GET request with an invalid card number
#         url = reverse('card-create-get')
#         response = self.client.get(url, {'card_number': '3422342342342'})
#
#         # Assert the response status code and error message
#         self.assertEqual(response.status_code, 404)
#         data = json.loads(response.content)
#         self.assertEqual(data['error'], 'Card not found')
#
#     def test_get_card_without_card_number(self):
#         # Make a GET request without providing a card number
#         url = reverse('card-create-get')
#         response = self.client.get(url)
#
#         # Assert the response status code and error message
#         self.assertEqual(response.status_code, 400)
#         data = json.loads(response.content)
#         self.assertEqual(data['error'], 'Please provide a card number.')
#
#     # Create a valid card data
#     def _generate_valid_card_data(self):
#         return {
#             'card_number': '6521938157614486',
#             'expiry_date': '12/23',
#             'cvv_code': '123',
#             'issue_date': '2023-01-01',
#             'owner_id': 'd4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e',
#             'card_status': 'active'
#         }
#
#     def test_create_valid_card(self):
#         # Create a valid card data
#         card_data = self._generate_valid_card_data()
#
#         # Make a POST request to create a valid card
#         url = reverse('card-create-get')
#         response = self.client.post(url, data=json.dumps(card_data), content_type='application/json')
#
#         # Assert the response status code and success message
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content)
#         self.assertEqual(data['message'], 'Card created successfully')
#
#     def test_create_invalid_card(self):
#         # Create an invalid card data with an invalid card number
#         card_data = self._generate_valid_card_data()
#         card_data['card_number'] = '4532015112893798'
#
#         # Make a POST request to create an invalid card
#         url = reverse('card-create-get')
#         response = self.client.post(url, data=json.dumps(card_data), content_type='application/json')
#
#         # Assert the response status code and error message
#         self.assertEqual(response.status_code, 400)
#         data = json.loads(response.content)
#         self.assertEqual(data['error'], 'Invalid card number.')
#
#
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


class CardViewTempTest(TestCase):
    # given
    def setUp(self):
        self.client = Client()
        self.card1 = Card.objects.create(card_number='1234567812345678', expiry_date='12/23', cvv_code='123', issue_date="2023-01-01", owner_id='d4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e')
        self.card2 = Card.objects.create(card_number='8765432187654321', expiry_date='10/24', cvv_code='456', issue_date="2023-01-01", owner_id='d4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e')

    def test_card_list_view(self):
        # when
        response = self.client.get(reverse('card_list'))
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards_list.html')
        self.assertContains(response, self.card1.card_number)
        self.assertContains(response, self.card2.card_number)


class CardCreateTempTest(TestCase):
    # given
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('create_card')
        self.save_url = reverse('save_card')
        self.valid_data = {
            'card_number': '1234567890123456',
            'expiry_date': '12/23',
            'cvv_code': '123',
            'issue_date': '2023-01-01',
            'owner_id': 'd4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e',
            'card_status': 'active'
        }

    def test_get_create_view(self):
        # when
        response = self.client.get(self.create_url)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_card.html')

    def test_post_save_card(self):
        # when
        initial_count = Card.objects.count()
        response = self.client.post(self.save_url, data=self.valid_data)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), initial_count + 1)

    def test_post_invalid_data(self):
        # given
        invalid_data = {
            'card_number': '1234',
            'expiry_date': '',
            'cvv_code': 'abc',
            'issue_date': '2023-01-01',
            'owner_id': 'd4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e',
            'card_status': 'active'
        }
        # when
        initial_count = Card.objects.count()
        response = self.client.post(self.save_url, data=invalid_data)
        # then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Card.objects.count(), initial_count)


class CardAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.client.login(username='admin', password='password')

    def test_card_list_display(self):
        Card.objects.create(
            card_number='5555444433332222',
            expiry_date='12/23',
            cvv_code='555',
            issue_date="2023-01-01",
            owner_id="d4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e",
            card_status="active"
        )

        list_url = reverse('admin:cards_card_changelist')
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5555444433332222')  # Check if card number is displayed in the response

    def test_card_creation(self):
        change_url = reverse('admin:cards_card_add')
        response = self.client.get(change_url)

        self.assertEqual(response.status_code, 200)

        data = {
            'card_number': '8888444488884444',
            'expiry_date': '12/23',
            'cvv_code': '848',
            'issue_date': '2023-01-01',
            'owner_id': 'd4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e',
            'card_status': 'active'
        }

        response = self.client.post(change_url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 1)

    def test_card_update(self):
        card = Card.objects.create(
            card_number='7777444433332222',
            expiry_date='12/23',
            cvv_code='555',
            issue_date="2023-01-01",
            owner_id="d4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e",
            card_status="active"
        )
        change_url = reverse('admin:cards_card_change', args=[card.id])
        response = self.client.get(change_url)

        self.assertEqual(response.status_code, 200)

        data = {
            'card_number': '9876543210987654',
            'expiry_date': '01/25',
            'cvv_code': '321',
            'issue_date': '2023-01-01',
            'owner_id': 'd4cb7f9b-4e4a-4f4e-9f55-eb80d013f90e',
            'card_status': 'new'
        }

        response = self.client.post(change_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check if the response after the redirect is 200

        card.refresh_from_db()
        self.assertEqual(card.card_number, '9876543210987654')
        self.assertEqual(card.expiry_date, '01/25')
        self.assertEqual(card.card_status, 'new')