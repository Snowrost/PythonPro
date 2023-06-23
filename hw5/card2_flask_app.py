import json

from flask import Flask, request
from card import Card, CardStatus, Role
from card_repository import CardRepository
from datetime import datetime


class CardAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.card_repo = CardRepository()
        self.app.route("/cards/get/<card_id>")(self.get_card_by_id)
        self.app.route("/cards/save", methods=["POST"])(self.save_card)

    def get_card_by_id(self, card_id):
        role = Role.USER  # "Set the role here"
        try:
            card = self.card_repo.get_card_by_id(card_id, role)
            if card is not None:
                card_data = {
                    "card_id": card.card_id,
                    "card_number": card.card_number,
                    "expiry_date": card.expiry_date,
                    "cvv_code": card.cvv_code,
                    "issue_date": card.issue_date.strftime("%m/%d/%y"),
                    "owner_id": str(card.owner_id),
                    "card_status": card.card_status,
                }
                return card_data, 200
            else:
                return "Card not found.", 402
        except PermissionError as e:
            return str(e), 403

    def save_card(self):
        card_data = request.json
        role = Role.USER  # Set the role here
        try:
            card = self.create_card_from_data(card_data)
            self.card_repo.save_card(card, role)
            return "Card saved successfully.", 200
        except PermissionError as e:
            return str(e), 403

    @staticmethod
    def create_card_from_data(card_data):
        card_id = card_data.get("card_id")
        card_number = card_data.get("card_number")
        expiry_date = card_data.get("expiry_date")
        cvv_code = card_data.get("cvv_code")
        issue_date = card_data.get("issue_date")
        owner_id = card_data.get("owner_id")
        card_status_str = card_data.get("card_status")
        card_status = CardStatus(card_status_str)
        return Card(
            card_id,
            card_number,
            expiry_date,
            cvv_code,
            issue_date,
            owner_id,
            card_status,
        )

    def run(self):
        self.app.run()


if __name__ == "__main__":
    card_api = CardAPI()
    card_api.run()
