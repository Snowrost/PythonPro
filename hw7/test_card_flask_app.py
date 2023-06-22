import pytest
from card import Card, CardStatus, RBAC
from card_repository import CardRepository
from card2_flask_app import CardAPI


class TestFlaskCardApp:

    # given
    @pytest.fixture()
    def sample_card(self):
        return Card(
            card_id="223",
            card_number="1234-5678-9012-3456",
            expiry_date="12/24",
            cvv_code="123",
            issue_date="01/01/22",
            owner_id="26d86dd9-816e-5587-b3ae-3a9416065a3a",
            card_status=CardStatus.NEW,
        )

    @pytest.fixture
    def card_repository(self):
        return CardRepository()

    @pytest.fixture
    def app(self):
        file_app = CardAPI()
        app = file_app.app
        app.testing = True
        return app
    @pytest.fixture()
    def client(self, app):
        return app.test_client()

    def test_flask_card_app_save_card(self, app, sample_card, card_repository,client):
        card_data = {
            "card_id": sample_card.card_id,
            "card_number": sample_card.card_number,
            "expiry_date": sample_card.expiry_date,
            "cvv_code": sample_card.cvv_code,
            "issue_date": sample_card.issue_date.strftime("%m/%d/%y"),
            "owner_id": sample_card.owner_id,
            "card_status": sample_card.card_status.value,
        }
        # when
        response = client.post("/cards/save", json=card_data)

        # then
        assert response.status_code == 200
        assert response.data.decode() == "Card saved successfully."

    def test_flask_card_app_get_card_by_id(self, app, sample_card, client):
        # when
        response = client.get(f"/cards/get/{sample_card.card_id}")

        # then
        assert response.status_code == 200

        # Verify the card data in the response
        card_data = response.get_json()
        assert card_data["card_id"] == sample_card.card_id
        assert card_data["card_number"] == sample_card.card_number
        assert card_data["expiry_date"] == sample_card.expiry_date
        assert card_data["cvv_code"] == sample_card.cvv_code
        assert card_data["issue_date"] == sample_card.issue_date.strftime("%m/%d/%y")
        assert card_data["owner_id"] == str(sample_card.owner_id)
        assert card_data["card_status"] == sample_card.card_status.value

    def test_get_card_by_id_not_found(self, app, client):
        # when
        response = client.get("/cards/get/999")
        # then
        assert response.status_code == 402
        assert response.data.decode() == "Card not found."
