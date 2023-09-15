from django import forms

from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'expiry_date', 'cvv_code', 'issue_date', 'owner_id']