from flask import Flask, jsonify, request

from DB_hw4 import get_customers

from typing import List, Set

app = Flask(__name__)

@app.route("/")
def hw_4_extra():
    return "<p><b>HW 4 extra Flask /n Реализовать вью-функцию Flask для функции get_customers()</b></p>"

@app.route("/customers", methods=["GET"])
def get_customer_app() -> List:
    '''
    functione serializes data from chinook.db on cuurent functione get_customers to JavaScript
    :return: serializes data
    '''
    state_name = request.args.get("state_name")
    city_name = request.args.get("city_name")
    records = get_customers(state_name, city_name)
    return jsonify(records)


if __name__ == "__main__":
    app.run()
