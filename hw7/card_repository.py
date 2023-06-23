from card import Card, RBAC
import psycopg2
import os

# Класс репозиторію


class CardRepository:
    def __init__(self):
        self.db_connection = self.connect()
        self.create_table()

    def connect(self):
        connection = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            dbname="test27",
            user="postgres",
            password=os.environ.get("DB_PASSWORD", "d87nv2at"),
        )
        return connection

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS cards (
            card_id TEXT PRIMARY KEY,
            card_number TEXT,
            expiry_date TEXT,
            cvv_code TEXT,
            issue_date TEXT,
            owner_id TEXT,
            card_status TEXT
        )
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        self.db_connection.commit()

    def save_card(self, card, role):
        rbac = RBAC()
        if not rbac.has_permission(role, "save_card"):
            raise PermissionError("Insufficient privileges to save card.")

        query = """
        INSERT INTO cards (card_id, card_number, expiry_date, cvv_code, issue_date, owner_id, card_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            card.card_id,
            card.card_number,
            card.expiry_date,
            card.cvv_code,
            card.issue_date.strftime("%m/%d/%y"),
            str(card.owner_id),
            card.card_status.value,
        )
        cursor = self.db_connection.cursor()
        cursor.execute(query, values)
        self.db_connection.commit()

    def get_card_by_id(self, card_id, role):
        rbac = RBAC()
        if not rbac.has_permission(role, "get_card_by_id"):
            raise PermissionError("Insufficient privileges to get card by ID.")

        query = """
        SELECT * FROM cards WHERE card_id = %s
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (card_id,))
        row = cursor.fetchone()
        if row is not None:
            return self.row_to_card(row)
        return None

    def row_to_card(self, row):
        (
            card_id,
            card_number,
            expiry_date,
            cvv_code,
            issue_date,
            owner_id,
            card_status,
        ) = row
        return Card(
            card_id,
            card_number,
            expiry_date,
            cvv_code,
            issue_date,
            owner_id,
            card_status,
        )

    def close(self):
        self.db_connection.close()
