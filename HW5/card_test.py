import pytest
from card import Card, CardStatus, Role, RBAC
from card_repository import CardRepository
import uuid
from datetime import datetime


class TestCard:
    @pytest.fixture
    def sample_card(self):
        return Card(
            card_id='123',
            card_number='1234-5678-9012-3456',
            expiry_date='12/24',
            cvv_code='123',
            issue_date='01/01/22',
            owner_id='578',
            card_status=CardStatus.NEW
        )

    def test_activate_card(self, sample_card):
        #given
        sample_card.card_status = CardStatus.ACTIVE
        #when
        sample_card.activate_card()
        #then
        assert sample_card.card_status == CardStatus.ACTIVE

        #given
        sample_card.card_status = CardStatus.BLOCKED
        # when
        with pytest.raises(ValueError):
            sample_card.activate_card()
        # then
        assert sample_card.card_status == CardStatus.BLOCKED

    def test_block_card(self, sample_card):
        sample_card.block_card()
        assert sample_card.card_status == CardStatus.BLOCKED

    def test_validate_card_number_valid(self, sample_card):
        # when
        sample_card.validate_card_number('1234-5678-9012-3456')
        # then: no exception should be raised

    def test_validate_card_number_invalid(self, sample_card):
        # when/then
        with pytest.raises(ValueError):
            sample_card.validate_card_number('1234567890123456')

    def test_log_incident(self, sample_card):
        # given
        incident_type = 'unusual_activity'
        description = 'Unauthorized transaction'

        # when
        sample_card.log_incident(incident_type, description)

        # then
        assert len(sample_card.incident_log) == 1
        incident = sample_card.incident_log[0]
        assert incident['incident_type'] == incident_type
        assert incident['description'] == description

    def test_log_incident_unusual_activity(self, sample_card, caplog):
        # given
        incident_type = 'unusual_activity'
        description = 'Unauthorized transaction'

        # when
        sample_card.log_incident(incident_type, description)

        # then
        assert 'Unusual activity detected' in caplog.text
        assert f"Unusual activity detected for card {sample_card.card_number}" in caplog.text
        assert description in caplog.text


    class TestCardRepository:
        @pytest.fixture
        def card_repository(self):
            return CardRepository(':memory:')

        def test_save_and_get_card_by_id_user(self, card_repository, sample_card):
            # given
            card_repository.save_card(sample_card, role=Role.USER)
            # when
            retrieved_card = card_repository.get_card_by_id('123', role=Role.USER)
            # then:
            assert retrieved_card is not None
            assert retrieved_card.card_id == '123'
            assert retrieved_card.card_number == '1234-5678-9012-3456'
            assert retrieved_card.expiry_date == '12/24'
            assert retrieved_card.verify_cvv_code('123')
            assert retrieved_card.issue_date == datetime.strptime('01/01/22', '%m/%d/%y')
            assert isinstance(retrieved_card.owner_id, uuid.UUID)
            assert retrieved_card.card_status == CardStatus.NEW.value

        def test_get_card_by_nonexistent_id(self, card_repository):
            # when
            retrieved_card = card_repository.get_card_by_id('nonexistent_id', role=Role.USER)
            # then:
            assert retrieved_card is None

        def test_save_non_user(self, card_repository, sample_card):
            with pytest.raises(PermissionError):
                card_repository.save_card(sample_card, role=Role.GUEST)

        def test_save_user_get_by_id_nonuser(self, card_repository, sample_card):
            card_repository.save_card(sample_card, role=Role.USER)
            with pytest.raises(PermissionError):
                card_repository.get_card_by_id('123', role=Role.GUEST)


        def test_close_connection(self, card_repository):
            card_repository.close()
            assert card_repository.conn.close