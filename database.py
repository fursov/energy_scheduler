#!/usr/bin/env python

import datetime
import logging
import sqlite3

SQLITE_DB_NAME = 'en_saver.db'
SQLITE_DEVICES_TABLE_NAME = 'devices'

logger = logging.getLogger(__name__)

class SqLiteDb():
    def __init__(self, name) -> None:
        logger.debug('Constructor')
        self.name = name

    def __enter__(self):
        logger.debug('Enter')
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        logger.debug('Exit')
        self.connection.close()

    def execute(self, command, expansion=None):
        logger.debug(f'Execute {command}')
        if expansion:
            result = self.cursor.execute(command, expansion)
        else:
            result = self.cursor.execute(command)
        return result

    def commit(self):
        self.connection.commit()

    def get_colunms(self):
        cols = self.cursor.description
        return (col[0] for col in cols)


def create_device_table():
    with SqLiteDb(SQLITE_DB_NAME) as db:
        db.execute(
            f"""CREATE TABLE IF NOT EXISTS "devices" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"consumption_1"	REAL DEFAULT 0.0,
	"consumption_2"	REAL DEFAULT 0.0,
	"consumption_3"	REAL DEFAULT 0.0,
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
               activity_period=datetime.time(),
               activity_duration=datetime.time(),
               delay_factor_on_peak_price_per_hour=0,
               max_delayed_debt=0):
    if isinstance(consumption, (int, float)):
        consumption = [consumption, 0, 0]
    if not isinstance(consumption, list):
        logger.error(f'Invalid consumption type for device "{name}"')
    if len(consumption) > 3:
        logger.error(f'Invalid consumption configuration for device "{name}", only 3 phases supported')
    period = activity_period.strftime('%H:%M:%S')
    duration = activity_duration.strftime('%H:%M:%S')
    with SqLiteDb(SQLITE_DB_NAME) as db:
        query = db.execute("SELECT * FROM {SQLITE_DEVICES_TABLE_NAME} WHERE name=:name;", {'name': name})
        if query.fetchall():
            logger.warning(f'Device "{name}" already exists')
            return
        db.execute(
            f"""INSERT INTO {SQLITE_DEVICES_TABLE_NAME}
                (name, consumption_1, consumption_2, consumption_3, period, duration, delay_factor, max_delay_debt)
                VALUES (:name, :consumption_1, :consumption_2, :consumption_3,
                        :period, :duration, :delay_factor, :max_delay_debt)""",
                {
                    'name': name,
                    'consumption_1': consumption[0],
                    'consumption_2': consumption[1],
                    'consumption_3': consumption[2],
                    'period': period,
                    'duration': duration,
                    'delay_factor': delay_factor_on_peak_price_per_hour,
                    'max_delay_debt': max_delayed_debt
                })
        db.commit()


def get_device(name):
    with SqLiteDb(SQLITE_DB_NAME) as db:
        query = db.execute(f"SELECT * FROM {SQLITE_DEVICES_TABLE_NAME} WHERE name=:name;", {'name': name})
        result = query.fetchall()
        if result:
            colunms = db.get_colunms()
            return dict(zip(colunms, result[0]))
        logger.warning(f'No device found with name "{name}"')
        return None


def get_all_devices():
    with SqLiteDb(SQLITE_DB_NAME) as db:
        query = db.execute(f"SELECT * FROM {SQLITE_DEVICES_TABLE_NAME};")
        results = query.fetchall()
        if results:
            colunms = db.get_colunms()
            return (dict(zip(colunms, res)) for res in results)
        logger.warning(f'No devices found')
        return None
