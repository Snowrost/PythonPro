from card import Card, RBAC
from enum import Enum
import sqlite3



# Класс репозоиторію

class CardRepository:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS cards (
            card_id TEXT PRIMARY KEY,
            card_number TEXT,
            expiry_date TEXT,
            cvv_code TEXT,
            issue_date TEXT,
            owner_id TEXT,
            card_status TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def save_card(self, card, role):
        rbac = RBAC()
        if not rbac.has_permission(role, 'save_card'):
            raise PermissionError('Insufficient privileges to save card.')

        query = '''
        INSERT INTO cards (card_id, card_number, expiry_date, cvv_code, issue_date, owner_id, card_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        values = (
            card.card_id,
            card.card_number,
            card.expiry_date,
            card.cvv_code,
            card.issue_date.strftime('%m/%d/%y'),
            str(card.owner_id),
            card.card_status.value
        )
        self.conn.execute(query, values)
        self.conn.commit()

    def get_card_by_id(self, card_id, role):
        rbac = RBAC()
        if not rbac.has_permission(role, 'get_card_by_id'):
            raise PermissionError('Insufficient privileges to get card by ID.')

        query = '''
        SELECT * FROM cards WHERE card_id = ?
        '''
        cursor = self.conn.execute(query, (card_id,))
        row = cursor.fetchone()
        if row is not None:
            return self.row_to_card(row)
        return None

    def row_to_card(self, row):
        card_id, card_number, expiry_date, cvv_code, issue_date, owner_id, card_status = row
        return Card(card_id, card_number, expiry_date, cvv_code, issue_date, owner_id, card_status)


    def close(self):
        self.conn.close()




