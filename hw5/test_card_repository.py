import pytest
from card import Card, CardStatus, Role, RBAC
from card_repository import CardRepository
import uuid
from datetime import datetime


@pytest.fixture
def rbac():
    return RBAC()


@pytest.fixture
def sample_card():
    return Card(
        card_id="123",
        card_number="1234-5678-9012-3456",
        expiry_date="12/24",
        cvv_code="123",
        issue_date="01/01/22",
        owner_id="26d86dd9-816e-5587-b3ae-3a9416065a3a",
        card_status=CardStatus.NEW,
    )


@pytest.fixture
def card_repository():
    return CardRepository()


class TestCardRepository:
    def test_save_and_get_card_by_id_user(self, card_repository, sample_card):
        # given
        card_repository.save_card(sample_card, role=Role.USER)
        # when
        retrieved_card = card_repository.get_card_by_id("123", role=Role.USER)
        # then:
        assert retrieved_card is not None
        assert retrieved_card.card_id == "123"
        assert retrieved_card.card_number == "1234-5678-9012-3456"
        assert retrieved_card.expiry_date == "12/24"
        assert retrieved_card.verify_cvv_code("123")
        assert retrieved_card.issue_date == datetime.strptime("01/01/22", "%m/%d/%y")
        assert isinstance(retrieved_card.owner_id, uuid.UUID)
        assert retrieved_card.card_status == CardStatus.NEW.value

    def test_get_card_by_nonexistent_id(self, card_repository):
        # when
        retrieved_card = card_repository.get_card_by_id(
            "nonexistent_id", role=Role.USER
        )
        # then:
        assert retrieved_card is None

    def test_save_non_user(self, card_repository, sample_card):
        with pytest.raises(PermissionError):
            card_repository.save_card(sample_card, role=Role.GUEST)

    def test_save_user_get_by_id_nonuser(self, card_repository, sample_card):
        sample_card.card_id = "222"
        card_repository.save_card(sample_card, role=Role.USER)
        with pytest.raises(PermissionError):
            card_repository.get_card_by_id("123", role=Role.GUEST)

    def test_close_connection(self, card_repository):
        card_repository.close()
        assert card_repository.db_connection.close
