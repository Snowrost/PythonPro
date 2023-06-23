import requests
from datetime import datetime
from urllib import parse


#print(get_currency_exchange_rate('USD', 'UAH'))



#HW 3 TODO додати функцію валідації формату дати

def validate_date_format(rate_date:str):
    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%m.%d.%Y",
        "%Y/%m/%d"
    ]
    desired_format = "%d.%m.%Y"
    for date_format in formats:
        try:
            formatted_date = datetime.strptime(rate_date, date_format).strftime(desired_format)
            return formatted_date
        except ValueError:
            continue
    return False



# HW 3 TODO додати валідацію банків

def validate_banks(bank:str):
    PB_formats = [
        "nbu",
        "nationalbank",
        "NationalBank",
        "NB"
    ]
    NB_formats = [
        "pb",
        "PB",
        "privatbank",
        "PrivatBank"
    ]
    if bank in PB_formats:
        bank = "PB"
    elif bank in NB_formats:
        bank = "NB"
    else:
        return False
    return bank

def get_pb_exchange_rate(convert_currency: str,
                         bank: str,
                         rate_date: str) -> str:
    if not validate_date_format(rate_date):
        return "Invalid date format"
    if not validate_banks(bank):
        return "Rates for this bank is not supported" # TODO Додати ще обробку випадку, коли клієнт ввів якийсь інший банк. Видавати повідомлення про помилку, наприклад: Rates for this bank is not supported

    rate_date_formatted = validate_date_format(rate_date)  # Adding date formating
    params = {
        'json': '',
        'date': rate_date_formatted,
    }
    query = parse.urlencode(params)
    api_url = 'https://api.privatbank.ua/p24api/exchange_rates?'
    response = requests.get(api_url+query)
    json = response.json()

    if response.status_code == 200:
        rates = json['exchangeRate']
        for rate in rates:
            if rate['currency'] == convert_currency:
                if bank == 'NB': #FIXED was NBU
                    try:
                        sale_rate = rate['saleRateNB']
                        purchase_rate = rate['purchaseRateNB']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date_formatted} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except:
                        return f'There is no exchange rate NBU for {convert_currency}'
                elif bank == 'PB':
                    try:
                        sale_rate = rate['saleRate']
                        purchase_rate = rate['purchaseRate']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date_formatted} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except:
                        return f'There is no exchange rate PrivatBank for {convert_currency}'
    else:
        return f'error {response.status_code}'


result = get_pb_exchange_rate('USD', 'NB', '2022-11-30')
print(result)