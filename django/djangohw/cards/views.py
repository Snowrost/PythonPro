import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.views import View

from .forms import CardForm
from .models import Card


# class CardView(View):
#     def get(self, request):
#         card_number = request.GET.get('card_number', None)
#         if card_number:
#             try:
#                 card = Card.objects.get(card_number=card_number)
#                 data = {
#                     'id': str(card.id),
#                     'card_number': card.card_number,
#                     'expiry_date': card.expiry_date,
#                     'cvv_code': card.cvv_code,
#                     'issue_date': card.issue_date.strftime('%Y-%m-%d'),
#                     'owner_id': str(card.owner_id),
#                     'card_status': card.card_status
#                 }
#                 return JsonResponse(data)
#             except ObjectDoesNotExist:
#                 return JsonResponse({'error': 'Card not found'}, status=404)
#         else:
#             return JsonResponse({'error': 'Please provide a card number.'}, status=400)
#
#     def post(self, request: HttpRequest):
#         # Parse the JSON data from the request body
#         data = json.loads(request.body)
#
#         # Create a new card object with the provided data
#         card = Card(
#             card_number=data['card_number'],
#             expiry_date=data['expiry_date'],
#             cvv_code=data['cvv_code'],
#             issue_date=data['issue_date'],
#             owner_id=data['owner_id'],
#             card_status=data['card_status']
#         )
#
#         # Check if the card number is valid
#         if not card.is_valid():
#             return JsonResponse({'error': 'Invalid card number.'}, status=400)
#
#         # Save the card object to the database
#         card.save()
#
#         # Return a success message
#         response_data = {'message': 'Card created successfully'}
#         return JsonResponse(response_data)


class CardViewTemp(View):
    def get(self, request):
        cards = Card.objects.all()
        context = {'cards': cards}
        return render(request, 'cards_list.html', context)


class CardCreateTemp(View):
    def get(self, request):
        form = CardForm()
        context = {'form': form}
        return render(request, 'create_card.html', context)

    def post(self, request):
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('card_list')
        else:
            context = {'form': form}
            return render(request, 'create_card.html', context, status=400)

