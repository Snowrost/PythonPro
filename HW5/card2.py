from enum import Enum
import uuid
from datetime import datetime


class CardStatus(Enum):
    NEW = 'new'
    ACTIVE = 'active'
    BLOCKED = 'blocked'

class Card:
    def __init__(self, card_id: str, card_number: str, expiry_date: str, cvv_code: str, issue_date: str, owner_id: str, card_status):
        self.card_id = card_id
        self.card_number = card_number
        self.expiry_date = expiry_date
        self._cvv_code = cvv_code
        self.issue_date = datetime.strptime(issue_date, '%m/%d/%y')
        self.owner_id = uuid.uuid5(uuid.NAMESPACE_DNS, owner_id)
        self.card_status = card_status

    def activate_card(self):
        if self.card_status == CardStatus.BLOCKED:
            raise ValueError('Blocked cards cannot be activated.')
        self.card_status = CardStatus.ACTIVE

    def block_card(self):
        self.card_status = CardStatus.BLOCKED

    #Фича Masking розумію що не найкраща. Але з енкритптою і декриптою не до кінця розібрався, а валідація вже і так у домашці була(
    @property
    def cvv_code(self):
        return '*' * len(self._cvv_code)

    @cvv_code.setter
    def cvv_code(self, value):
        self._cvv_code = value
