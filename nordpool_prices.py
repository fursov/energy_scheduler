#!/usr/bin/env python

import datetime
import logging
import pytz

from nordpool import elspot

logger = logging.getLogger(__name__)

FI_VAT = 1.24
FI_TIMEZONE = pytz.timezone('Europe/Helsinki')


def get_prices():
    prices_spot = elspot.Prices()
    try:
        prices_spot_finland_today = prices_spot.hourly(end_date=datetime.date.today(), areas=['FI'])
    except ConnectionError:
        logger.warning('Could not fetch nordpool today\'s prices!')
        return []
    prices = [{
            'time': data['start'].astimezone(FI_TIMEZONE),
            'value': round(data['value'] / 10.0 * FI_VAT, 2),
        } for data in prices_spot_finland_today['areas']['FI']['values'] if data['value'] != float('inf')]
    try:
        prices_spot_finland_tomorrow = \
            prices_spot.hourly(end_date=datetime.date.today() + datetime.timedelta(days=1), areas=['FI'])
    except ConnectionError:
        logger.warning('Could not fetch nordpool tomorrow\'s prices!')
        return prices
    prices.extend([{
            'time': data['start'].astimezone(FI_TIMEZONE),
            'value': round(data['value'] / 10.0 * FI_VAT, 2),
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
