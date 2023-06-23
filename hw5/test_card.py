import pytest
from card import Card, CardStatus, Role, RBAC
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


class TestCard:
    def test_rbac_has_permission(self, rbac):
        assert rbac.has_permission(Role.USER, "save_card")
        assert not rbac.has_permission(Role.GUEST, "save_card")
        assert rbac.has_permission(Role.USER, "get_card_by_id")
        assert not rbac.has_permission(Role.GUEST, "get_card_by_id")

    def test_card_creation(self, sample_card):
        assert sample_card.card_id == "123"
        assert sample_card.card_number == "1234-5678-9012-3456"
        assert sample_card.expiry_date == "12/24"
        assert sample_card.cvv_code == "123"
        assert isinstance(sample_card.issue_date, datetime)
        assert sample_card.owner_id == uuid.UUID("26d86dd9-816e-5587-b3ae-3a9416065a3a")
        assert sample_card.card_status == CardStatus.NEW

    def test_activate_card(self, sample_card):
        # given
        sample_card.card_status = CardStatus.ACTIVE
        # when
        sample_card.activate_card()
        # then
        assert sample_card.card_status == CardStatus.ACTIVE

    def test_card_block(self, sample_card):
        sample_card.block_card()
        assert sample_card.card_status == CardStatus.BLOCKED

    def test_card_number_validation(self, sample_card):
        with pytest.raises(ValueError):
            sample_card.validate_card_number("1234567890123456")

    def test_card_cvv_code_verification(self, sample_card):
        assert sample_card.verify_cvv_code("123")
        assert not sample_card.verify_cvv_code("456")

    def test_card_log_incident(self, sample_card):
        incident_type = "unusual_activity"
        description = "Suspicious transaction"
        sample_card.log_incident(incident_type, description)
        incident_log = sample_card.get_incident_log()
        assert len(incident_log) == 1
        assert incident_log[0]["incident_type"] == incident_type
        assert incident_log[0]["description"] == description
