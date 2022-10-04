#!/usr/bin/env python

import datetime
import logging
import pytz

from nordpool import elspot

logger = logging.getLogger(__name__)

FI_TIMEZONE = pytz.timezone('Europe/Helsinki')
FI_LOW_TAX_RATE_START = datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=FI_TIMEZONE)
FI_LOW_TAX_RATE_END = datetime.datetime(2023, 4, 30, 23, 59, 59, tzinfo=FI_TIMEZONE)
FI_REGULAR_VAT = 1.24
FI_LOW_VAT = 1.10


def get_past_prices(days_before=0):
    prices_spot = elspot.Prices()
    now = datetime.datetime.now(tz=FI_TIMEZONE)
    tax_rate = FI_REGULAR_VAT if now < FI_LOW_TAX_RATE_START or now > FI_LOW_TAX_RATE_END else FI_LOW_VAT
    try:
        prices_spot_finland = prices_spot.hourly(end_date=datetime.date.today() - datetime.timedelta(days=days_before), areas=['FI'])
    except ConnectionError:
        logger.warning('Could not fetch nordpool today\'s prices!')
        return []
    prices = [{
            'time': data['start'].astimezone(FI_TIMEZONE),
            'value': round(data['value'] / 10.0 * tax_rate, 2),
        } for data in prices_spot_finland['areas']['FI']['values'] if data['value'] != float('inf')]
    return prices


def get_prices():
    prices_spot = elspot.Prices()
    now = datetime.datetime.now(tz=FI_TIMEZONE)
    tax_rate = FI_REGULAR_VAT if now < FI_LOW_TAX_RATE_START or now > FI_LOW_TAX_RATE_END else FI_LOW_VAT
    try:
        prices_spot_finland_today = prices_spot.hourly(end_date=datetime.date.today(), areas=['FI'])
    except ConnectionError:
        logger.warning('Could not fetch nordpool today\'s prices!')
        return []
    prices = [{
            'time': data['start'].astimezone(FI_TIMEZONE),
            'value': round(data['value'] / 10.0 * tax_rate, 2),
        } for data in prices_spot_finland_today['areas']['FI']['values'] if data['value'] != float('inf')]
    try:
        prices_spot_finland_tomorrow = \
            prices_spot.hourly(end_date=datetime.date.today() + datetime.timedelta(days=1), areas=['FI'])
    except ConnectionError:
        logger.warning('Could not fetch nordpool tomorrow\'s prices!')
        return prices
    prices.extend([{
            'time': data['start'].astimezone(FI_TIMEZONE),
            'value': round(data['value'] / 10.0 * tax_rate, 2),
        } for data in prices_spot_finland_tomorrow['areas']['FI']['values'] if data['value'] != float('inf')])
    return prices


def get_future_prices():
    future_prices = []
    prices = get_prices()
    time_now = datetime.datetime.now(FI_TIMEZONE).replace(minute=0, second=0, microsecond=0)
    for data in prices:
        start_hour = data['time']
        if start_hour >= time_now:
            future_prices.append(data)
    return future_prices
