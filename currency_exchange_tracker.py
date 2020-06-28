#
# Currency Exchange Tracker
# Simple Command-Line style program to check currency exchange rate based on The European Central Bank (ECB) data
#
# Copyright (c) KvinTanaka. (MIT License)
# https://www.kvintanaka.com
#

import sys
import requests
from datetime import date, timedelta


# --- Currency Exchange Tracker - Main ---


def get_currency(currency_from, currency_to):
    """Get Currency Exchange Rate
    Currency data is taken from exchangeratesapi.io
    Which data sourced from The European Central Bank (ECB)
    Author: KvinTanaka"""

    api = "https://api.exchangeratesapi.io/latest?base=" + currency_to + "&symbols=" + currency_from
    response = requests.get(api)
    result = response.json()

    exchange_rates = result['rates'][currency_from]
    current_date = result['date']

    return {'rates': int(exchange_rates), 'date': current_date}


def get_past_currency(currency_to, currency_from, days):
    """Get Currency Exchange Rate for the specified time range (days)
    Currency data is taken from exchangeratesapi.io
    Author: KvinTanaka"""

    start_date = date.today() - timedelta(days=days)
    end_date = date.today()

    api = "https://api.exchangeratesapi.io/history?start_at=" + start_date.isoformat() + "&end_at=" + end_date.isoformat() + "&base=" + currency_from + "&symbols=" + currency_to
    response = requests.get(api)
    results = response.json()

    past_data = []
    for data in results['rates'].items():
        exchange_rates = data[1][currency_to]
        past_data.append({'rates': int(exchange_rates), 'date': data[0]})

    return past_data


def get_currency_statistic(past_data):
    """Calculate high, low, average, and trend from the past currency data
    Currency data is taken from exchangeratesapi.io
    Author: KvinTanaka"""

    lowest_rates = past_data[0]['rates']
    highest_rates = past_data[0]['rates']
    average_rates = 0

    # Trend here is a comparison between data yesterday and today
    if past_data[-1]['rates'] > past_data[-2]['rates']:
        trend = 'Up'
    else:
        trend = 'Down'

    # Calculate low, high, and average from the past data
    for data in past_data:
        if data['rates'] < lowest_rates:
            lowest_rates = data['rates']

        if data['rates'] > highest_rates:
            highest_rates = data['rates']

        average_rates += data['rates']
    average_rates = average_rates / len(past_data)

    return {'low': int(lowest_rates), 'average': int(average_rates), 'high': int(highest_rates), 'trend': trend}


def main():
    """Start Point"""
    currency_from = str(sys.argv[1]).upper()
    currency_to = str(sys.argv[2]).upper()

    data = get_currency(currency_from, currency_to)
    past_data = get_past_currency(currency_from, currency_to, 30)
    data_statistic = get_currency_statistic(past_data)

    print("Date: " + str(data['date']))
    print(currency_from + " to " + currency_to + " rate: " + str(data['rates']))
    print("Trend: " + str(data_statistic['trend']))

    print("\nData from past " + str(30) + " days:")
    print("High: " + str(data_statistic['high']))
    print("Low: " + str(data_statistic['low']))
    print("Average: " + str(data_statistic['average']))


if __name__ == "__main__":
    main()

