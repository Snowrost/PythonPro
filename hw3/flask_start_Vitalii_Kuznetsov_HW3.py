from flask import Flask, request

from utils_Vitalii_Kuznetsov_HW3 import get_pb_exchange_rate

app = Flask(__name__)

@app.route("/rates_pb", methods=['GET'])
def get_pb_rates():
    convert_currency = request.args.get('convert_currency', default='USD')
    bank = request.args.get('bank', default='NBU') # TODO додати функцію валідації вводу банку
    rate_date = request.args.get('rate_date', default='01.11.2022')
    result = get_pb_exchange_rate(convert_currency, bank, rate_date)
    return result