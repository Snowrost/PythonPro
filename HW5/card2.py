from enum import Enum
import uuid
from datetime import datetime
import re
import hashlib


'''Фічя розділ прав дотсупу 
'''


class Role(Enum):
    USER = 'user'
    NONUSER = 'nonuser'


class RBAC:
    def __init__(self):
        self.role_permissions = {
            Role.USER: ['save_card', 'get_card_by_id'],
            Role.NONUSER: []
        }
    def has_permission(self, role: Role, action: str) -> bool:
        permissions = self.role_permissions.get(role, [])
        return action in permissions


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
        self.set_cvv_code(cvv_code)
    def activate_card(self):
        if self.card_status == CardStatus.BLOCKED:
            raise ValueError('Blocked cards cannot be activated.')
        self.card_status = CardStatus.ACTIVE

    def block_card(self):
        self.card_status = CardStatus.BLOCKED

    def validate_card_number(self, card_number: str):
        # Validate card number format using a regular expression
        pattern = r'^\d{4}-\d{4}-\d{4}-\d{4}$'
        if not re.match(pattern, card_number):
            raise ValueError('Invalid card number format. Please use the format XXXX-XXXX-XXXX-XXXX.')

    def set_cvv_code(self, cvv_code):
        # Hash the cvv_code using sha256 and store the hashed value
        self.cvv_code_hash = hashlib.sha256(cvv_code.encode()).hexdigest()

    def verify_cvv_code(self, cvv_code):
        # Verify if the provided cvv_code matches the stored hashed value
        hashed_cvv_code = hashlib.sha256(cvv_code.encode()).hexdigest()
        return self.cvv_code_hash == hashed_cvv_code



