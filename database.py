#!/usr/bin/env python

import datetime
import sqlite3
from types import NoneType

SQLITE_DB_NAME = 'energy_scheduler.db'
SQLITE_DEVICES_TABLE_NAME = 'scheduling_devices'


class SqLiteDb():
    def __init__(self, name) -> None:
        print('Constructor')
        self.name = name

    def __enter__(self):
        print('Enter')
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('Exit')
        self.connection.close()

    def execute(self, command):
        print(f'Execute {command}')
        return self.cursor.execute(command)

    def commit(self):
        self.connection.commit()


def create_device_table():
    with SqLiteDb(SQLITE_DB_NAME) as db:
        db.execute(
            f"""CREATE TABLE IF NOT EXISTS "devices" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"consumption"	REAL,
	"phases"	INTEGER,
	"period"	TEXT NOT NULL,
	"duration"	TEXT NOT NULL,
	"last_activated"	INTEGER NOT NULL DEFAULT 0,
	"delay_factor"	REAL DEFAULT 1.0,
	"max_delay_debt"	REAL NOT NULL DEFAULT 1.0,
	"current_delay_debt"	REAL DEFAULT 0.0,
	"enabled"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")


def add_device(name,
               consumption,
               phase_lines=None,
               activity_period=datetime.time(),
               activity_duration=datetime.time(),
               delay_factor_on_peak_price_per_hour=0,
               max_delayed_debt=0):
    phases = sum(2**(line - 1) for line in phase_lines) if phase_lines else 0
    period = activity_period.strftime('%H:%M:%S')
    duration = activity_duration.strftime('%H:%M:%S')
    with SqLiteDb(SQLITE_DB_NAME) as db:
        query = db.execute(f"SELECT * FROM {SQLITE_DEVICES_TABLE_NAME} WHERE name='{name}';")
        if query:
            print(f'Error! Device {name} exists')
        db.execute(
            f"""INSERT INTO {SQLITE_DEVICES_TABLE_NAME}
                (name, consumption, phases, period, duration, delay_factor, max_delay_debt)
                VALUES
                    ({name}, {consumption}, {phases}, {period}, {duration},
                     {delay_factor_on_peak_price_per_hour}, {max_delayed_debt})""")
        db.commit()


def get_device(name):
    with SqLiteDb(SQLITE_DB_NAME) as db:
        query = db.execute(f"SELECT * FROM {SQLITE_DEVICES_TABLE_NAME} WHERE name='{name}';")
        if query:
            return query.fetchall()
        return None
