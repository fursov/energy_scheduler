#!/usr/bin/env python

import datetime

import scheduler


def make_price_data_from_list(start_datetime, prices):
    return tuple({
        'time': start_datetime + datetime.timedelta(hours=1 * i),
        'value': price,
    } for i, price in enumerate(prices))



def test_find_window_for_power_duration():
    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    prices = make_price_data_from_list(now, (1, 2, 3, 4, 5, 6, 7, 8, 9))
    t = scheduler.find_window_for_power_duration(prices, 3)
    assert t == now

    prices = make_price_data_from_list(now, (5, 4, 3, 2, 1, 2, 3, 4, 5))
    t = scheduler.find_window_for_power_duration(prices, 3)
    assert t == now + datetime.timedelta(hours=3)
    t = scheduler.find_window_for_power_duration(prices, 2.5)
    assert t == now + datetime.timedelta(hours=3)
    t = scheduler.find_window_for_power_duration(prices, 1.5)
    assert t == now + datetime.timedelta(hours=3, minutes=30)

    prices = make_price_data_from_list(now, (5, 5, 2, 1, 1, 1, 3, 7, 5, 3, 4))
    t = scheduler.find_window_for_power_duration(prices, 3)
    assert t == now + datetime.timedelta(hours=3)
    t = scheduler.find_window_for_power_duration(prices, 5)
    assert t == now + datetime.timedelta(hours=2)
    t = scheduler.find_window_for_power_duration(prices, 6)
    assert t == now + datetime.timedelta(hours=1)

    prices = make_price_data_from_list(now, (5, 8, 2, 1, 7, 1, 3, 7, 5, 3, 4))
    t = scheduler.find_window_for_power_duration(prices, 3)
    assert t == now + datetime.timedelta(hours=3)
    t = scheduler.find_window_for_power_duration(prices, 4)
    assert t == now + datetime.timedelta(hours=2)

    prices = make_price_data_from_list(now, (5, 6, 7, 3, 2, 6, 6, 2, 4, 6, 6))
    t = scheduler.find_window_for_power_duration(prices, 1)
    assert t == now + datetime.timedelta(hours=4)
    t = scheduler.find_window_for_power_duration(prices, 1.5)
    assert t == now + datetime.timedelta(hours=3, minutes=30)
