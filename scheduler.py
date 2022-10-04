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


def find_start_time_for_power_duration(prices, duration):
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


def find_mean_value(prices):
    values = sorted(prices, key=lambda x: x['value'])
    vals = [v['value'] for v in values]
    print(vals)
    diffs = [round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])]
    print(diffs)
    return values[len(values) // 2]


def find_average_value(prices):
    total = sum(v['value'] for v in prices)
    return total // len(prices)


def find_flat_periods(prices, variation=0.1):
    pass


def get_low_prices(prices):
    all_slices = []
    average = find_average_value(prices)
    slice_started = False
    for price in prices:
        if price['value'] < average:
            if not slice_started:
                slice = [price['value']]
                slice_started = True
            else:
                slice.append(price['value'])
        else:
            if slice_started:
                slice_started = False
                all_slices.append(slice)
    if slice_started:
        all_slices.append(slice)
    return all_slices


if __name__ == '__main__':
    print('now')
    prices = nordpool_prices.get_future_prices()
    prices = prices[:24]
    vals = [p['value'] for p in prices]
    print(vals)
    print(get_low_prices(prices))
    print([round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])])
    print(find_mean_value(prices))
    print(find_average_value(prices))


    print('day_before=1')
    prices = nordpool_prices.get_past_prices(days_before=1)
    vals = [p['value'] for p in prices]
    print(vals)
    print(get_low_prices(prices))
    print([round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])])
    print(find_mean_value(prices))
    print(find_average_value(prices))

    print('day_before=2')
    prices = nordpool_prices.get_past_prices(days_before=2)
    vals = [p['value'] for p in prices]
    print(vals)
    print(get_low_prices(prices))
    print([round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])])
    print(find_mean_value(prices))
    print(find_average_value(prices))

    print('day_before=3')
    prices = nordpool_prices.get_past_prices(days_before=3)
    vals = [p['value'] for p in prices]
    print(vals)
    print(get_low_prices(prices))
    print([round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])])
    print(find_mean_value(prices))
    print(find_average_value(prices))

    print('day_before=4')
    prices = nordpool_prices.get_past_prices(days_before=4)
    vals = [p['value'] for p in prices]
    print(vals)
    print(get_low_prices(prices))
    print([round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])])
    print(find_mean_value(prices))
    print(find_average_value(prices))

    print('day_before=5')
    prices = nordpool_prices.get_past_prices(days_before=5)
    vals = [p['value'] for p in prices]
    print(vals)
    print(get_low_prices(prices))
    print([round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])])
    print(find_mean_value(prices))
    print(find_average_value(prices))

    print('day_before=6')
    prices = nordpool_prices.get_past_prices(days_before=6)
    vals = [p['value'] for p in prices]
    print(vals)
    print(get_low_prices(prices))
    print([round((n-v) / n, 2) for v, n in zip(vals[:-1], vals[1:])])
    print(find_mean_value(prices))
    print(find_average_value(prices))
