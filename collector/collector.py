#!/usr/bin/env python
# Reads from rtl_433, collects samples, and inserts into postgres database

from __future__ import print_function
import subprocess
import json
import time
import psycopg2
import psycopg2.extras

# Max rate to write samples to database. May be slower than this depending on sensor read rate, but will not be faster.
sample_rate_secs = 60
# rtl_433 command line args
rtl_cmd = ["rtl_433", "-q", "-R", "20", "-F", "json"]
# Postgres connect deets
db_config = 'host=127.0.0.1 port=5432 user=hotapp password=hothouse dbname=hothouse'

# Continuously reads from rtl_433 and yeilds output
def rtl_loop(cmd):
    print('Starting RTL subprocess')
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


# Read json from string. Doesn't freak out if it's not really json
def read_json(raw):
    try:
        return json.loads(raw)
    except ValueError, e:
        return None


# Save the collected samples to postgres
def upload_sample(samples, cursor):
    for key in samples:
        cursor.execute('INSERT INTO samples(sensor_id, read_dt, data) VALUES (%s, NOW(), %s)', (key, json.dumps(samples[key])))
    print('Saved %s samples' % len(samples))


# Connect to postgres
def connect_db():
    try:
        db_conn = psycopg2.connect(db_config)
        db_conn.set_session(autocommit=True)
        cursor = db_conn.cursor()
        print('Database connection established')
        return cursor
    except Exception as err:
        print('Error connecting to database!')
        print(err)
        sys.exit(-1)


db_cursor = connect_db()
last = time.time()
sample = {}
count = 0

# Process loop, only keep the last update from each device within the sample_rate_secs limit
for raw_line in rtl_loop(rtl_cmd):
    obj = read_json(raw_line)
    if obj:
        # Ambient Weather device
        if 'model' in obj and 'Ambient Weather' in obj['model']:
            sample['%i_%i' % (obj['device'], obj['channel'])] = obj
        else:
            print('Unknown data read: %s' % obj)
    else:
        print('Failed to read data from RTL: %s' % raw_line)

    current = time.time()
    if current >= last + sample_rate_secs:
        last = current
        count = count + 1
        upload_sample(sample, db_cursor)
        sample = {}
