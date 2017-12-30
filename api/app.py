from flask import Flask
import json
import datetime
import psycopg2
import psycopg2.extras

# Postgres connect deets
db_config = 'host=127.0.0.1 port=5432 user=hotapp password=hothouse dbname=hothouse'
app = Flask(__name__)
json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)


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


def extract(rows):
    ret = []
    for row in rows:
        ret.append(row[0])
    return ret


@app.route('/sensor/all')
def get_all():
	db_cursor.execute('SELECT data FROM latest')
	rows = db_cursor.fetchall()
	return json.dumps(extract(rows))


@app.route('/sensor/<id>')
def show_results(id):
    db_cursor.execute("SELECT data FROM sample WHERE sensor_id=%s ORDER BY read_dt LIMIT 100;", (id,))
    rows = db_cursor.fetchall()
    return json.dumps(extract(rows))


db_cursor = connect_db()

if __name__ == '__main__':
    app.run()
