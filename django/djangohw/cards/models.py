import uuid

from django.db import models


class Card(models.Model):
    CARD_STATUS = (
        ('new', 'New'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=7)  # Assuming month/year format (e.g., 12/23)
    cvv_code = models.CharField(max_length=3)
    issue_date = models.DateField()
    owner_id = models.UUIDField()
    card_status = models.CharField(max_length=10, choices=CARD_STATUS, default='new')

    def is_valid(self):
        card_number = self.card_number.replace(" ", "")  # Remove any spaces from the card number

        # Perform the Luhn check
        checksum = 0
        num_digits = len(card_number)
        odd_even = num_digits & 1

        for i in range(num_digits):
            digit = int(card_number[i])

            if i % 2 == odd_even:
                digit *= 2
                if digit > 9:
                    digit -= 9

            checksum += digit

        return checksum % 10 == 0
