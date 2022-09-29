#!/usr/bin/env python

import datetime


class Device():
    def __init__(self,
                 name='',
                 phase_lines=None,
                 consumption=0,
                 activity_period=datetime.time(),
                 activity_duration=datetime.time(),
                 delay_factor_on_peak_price_per_hour=0,
                 max_delayed_debt=0) -> None:
        self.name = name
        self.phase_lines = phase_lines
        self.consumption = consumption
        self.activity = {
            'period': activity_period,
            'duration': activity_duration,
        }
        self.started = False
        self.last_started = None
        self.scheduled_start = datetime.datetime(0, 0, 0)
        self.scheduled_end = datetime.datetime(0, 0, 0)
        self.delay_factor = delay_factor_on_peak_price_per_hour
        self.max_delayed_debt = max_delayed_debt
        self.current_delay_debt = 0
        self.enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled

    def activate(self):
        self.started = True
        self.last_started = datetime.datetime.now()
        self.scheduled_end = self.last_started + self.activity['min_duration']

    def release(self):
        self.started = False

    def time_to_end(self):
        if self.started:
            return self.scheduled_end - datetime.datetime.now()
        return None

    def time_to_start(self):
        if not self.started:
            return self.scheduled_start - datetime.datetime.now()
        return None

    def schedule_start(self, start_time):
        self.scheduled_start = start_time

    def delay(self):
        self.current_delay_debt += self.delay_factor
        return self.current_delay_debt <= self.max_delayed_debt
