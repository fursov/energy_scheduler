#!/usr/bin/env python

import datetime

from math import ceil

import database
import device
import nordpool_prices


class Scheduler():
    def __init__(self) -> None:
        pass


def get_all_enabled_devices():
    devices = database.get_all_devices()


def find_lowest_price_for_device(device):
    pass


def find_window_for_power_duration(prices, duration):
    window = ceil(duration * 2)
    # Double the data to get the 30-minutes resolution
    half_hour_prices = []
    for data in prices:
        half_hour_prices.append(data)
        half_hour_prices.append({
            'time': data['time'] + datetime.timedelta(minutes=30),
            'value': data['value'],
        })
    print(half_hour_prices)
    half_hour_windows = (half_hour_prices[i:i + window] for i in range(len(half_hour_prices) - window + 1))
    window_totals = tuple(sum(map(lambda x: x['value'], window_prices)) for window_prices in half_hour_windows)
    print(window_totals)
    min_price = min(window_totals)
    min_price_index = window_totals.index(min_price)
    return half_hour_prices[min_price_index]['time']
