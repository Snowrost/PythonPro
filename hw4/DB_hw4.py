import os
import sqlite3

from typing import List, Set


def execute_query(query_sql: str) -> List:
    """
    функція для виконная запитів
    :param query_sql: запит
    :return: результат запиту
    """
    db_loc = os.path.join(os.getcwd(), "chinook.db")
    connection = sqlite3.connect(db_loc)
    cursr = connection.cursor()
    result = cursr.execute(query_sql)
    return connection, cursr, result


# HW4 TODO Реализовать функцию, которая выведет прибыль по таблице invoice_items. Сумма по заказу = UnitPrice * Quantity
def calculate_profit() -> float:
    """
    functione calculate profit  from invoice_items
    :param query_sql: query
    :return:  profir and total_profit
    """
    query_sql = f"""
        SELECT UnitPrice
               ,Quantity
          FROM invoice_items
    """
    connection, cursor, result = execute_query(query_sql)
    profits = []
    for row in result:
        price = row[0]
        quantity = row[1]
        profit = price * quantity
        profits.append(profit)

    total_profit = sum(profits)
    cursor.close()
    connection.close()

    return total_profit


print(calculate_profit())

# TODO Реализовать функцию, которая выведет повторяющиеся FirstName из таблицы customers и кол-во их вхождений в таблицу


def get_customers_repeated() -> List:
    '''
    functione calculate all repeated customers
    :param query_sql: query
    :return: customers that was reapeted and counts of reapet
    '''
    query_sql = """
        SELECT FirstName            
          FROM customers
        """
    connection, cursor, records = execute_query(query_sql)

    firstnames = [row[0] for row in records]
    repeated_firstnames = {
        name: firstnames.count(name)
        for name in firstnames
        if firstnames.count(name) > 1
    }
    cursor.close()
    connection.close()
    return repeated_firstnames


print(get_customers_repeated())


# TODO Реализовать вью-функцию Flask для функции get_customers()
def get_customers(state_name: str = None, city_name: str = None) -> List:
    '''
    functione collect firstname from customers with filters
    :param query_sql: query
    :return: firstnames of costumers
    '''
    query_sql = """
        SELECT FirstName
              ,City 
              ,State
          FROM customers
        """
    filter_query = ""
    if city_name and state_name:
        filter_query = f" WHERE City = '{city_name}' and State = '{state_name}'"
    if city_name and not state_name:
        filter_query = f" WHERE City = '{city_name}'"
    if state_name and not city_name:
        filter_query = f" WHERE State = '{state_name}'"

    query_sql += filter_query
    connection, cursor, result = execute_query(query_sql)
    first_names_colector = [record[0] for record in result]
    connection.close()
    return first_names_colector


print(get_customers(city_name='Budapest'))
