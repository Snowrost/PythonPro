import pytest
from card2 import Card, CardStatus
from card_repository2 import CardRepository
from datetime import datetime
import sqlite3
import uuid


class TestCard:
    @pytest.fixture
    def sample_card(self):
        return Card(
            card_id='123',
            card_number='1234567890123456',
            expiry_date='12/24',
            cvv_code='123',
            issue_date='01/01/22',
            owner_id='example@example.com',
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

    def test_cvv_code(self, sample_card):
        masked_cvv_code = "***"
        assert sample_card.cvv_code == masked_cvv_code

    def test_set_cvv_code(self, sample_card):
        new_cvv_code = "456"
        sample_card.cvv_code = new_cvv_code
        assert sample_card.cvv_code == "***"
        assert sample_card._cvv_code == new_cvv_code  # Verify the actual value is updated

    class TestCardRepository:
        @pytest.fixture
        def card_repository(self):
            return CardRepository(':memory:')

        def test_save_and_get_card_by_id(self, card_repository, sample_card):
            # given
            card_repository.save_card(sample_card)
            # when
            retrieved_card = card_repository.get_card_by_id('123')
            # then:
            assert retrieved_card is not None
            assert retrieved_card.card_id == '123'
            assert retrieved_card.card_number == '1234567890123456'
            assert retrieved_card.expiry_date == '12/24'
            assert retrieved_card.cvv_code == '***'
            assert retrieved_card.issue_date == datetime.strptime('01/01/22', '%m/%d/%y')
            assert isinstance(retrieved_card.owner_id, uuid.UUID)
            assert retrieved_card.card_status == CardStatus.NEW.value

        def test_get_card_by_nonexistent_id(self, card_repository):
            # when
            retrieved_card = card_repository.get_card_by_id('nonexistent_id')
            # then:
            assert retrieved_card is None

        def test_close_connection(self, card_repository):
            card_repository.close()
            assert card_repository.conn.close