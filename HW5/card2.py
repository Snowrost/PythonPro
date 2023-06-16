from enum import Enum
import uuid
from datetime import datetime
import re


class CardStatus(Enum):
    NEW = 'new'
    ACTIVE = 'active'
    BLOCKED = 'blocked'

class Card:
    def __init__(self, card_id: str, card_number, expiry_date: str, cvv_code: str, issue_date: str, owner_id: str, card_status):
        self.card_id = card_id
        self.validate_card_number(card_number)
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv_code = cvv_code
        self.issue_date = datetime.strptime(issue_date, '%m/%d/%y')
        self.owner_id = uuid.uuid5(uuid.NAMESPACE_DNS, owner_id)
        self.card_status = card_status

    def activate_card(self):
        if self.card_status == CardStatus.BLOCKED:
            raise ValueError('Blocked cards cannot be activated.')
        self.card_status = CardStatus.ACTIVE

    def block_card(self):
        self.card_status = CardStatus.BLOCKED

    #Фича Data Validatione card number
    def validate_card_number(self, card_number: str):
        # Validate card number format using a regular expression
        pattern = r'^\d{4}-\d{4}-\d{4}-\d{4}$'
        if not re.match(pattern, card_number):
            raise ValueError('Invalid card number format. Please use the format XXXX-XXXX-XXXX-XXXX.')

