import settings

import csv
import time

import couchdb


couch = couchdb.Server(settings.DB_URL)


def get_or_create_db(db_name):
    try:
        db = couch[db_name]
    except couchdb.http.ResourceNotFound:
        print('creating db: ' + db_name)
        db = couch.create(db_name)
    return db


def write_proxies():
    db = get_or_create_db('proxies')
    del db
    db = get_or_create_db('proxies')
    with open('proxies.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        print('writing proxies...')
        for row in reader:
            gateway = True if row['Gateway'] == 'Ja' else False,
            print(gateway)
            doc = {
                'ip': row['IP'],
                'port': row['Port'],
                'url': '{}:{}'.format(row['IP'], row['Port']),
                'gateway': True if row['Gateway'] == 'Ja' else False,
                'anonymityLevel': int(row['Level']) if row['Level'] else -1,
                'time': float(row['Zeit'][:-5]),
                'online': int(row['Online'].strip()[:-1]),
                'lastUsed': int(time.time()) - 2 * 60 * 60,
                'burned': int(time.time()) - 1 * 60 * 60 if gateway else 1488449019,
            }
            print(doc)
            db.save(doc)


def get_proxy():
    timestamp = int(time.time())
    two_hours_ago = timestamp - 2 * 60 * 60
    db = get_or_create_db('proxies')

    unburned = '''function(doc) {{
    var oldest = 
        if (doc.burned < {})
            emit(doc.name, null);
    }}'''.format(two_hours_ago)
    proxies = db.query(unburned)
    for row in db.query(unburned):
        print(row['id'])
    from ipdb import set_trace; set_trace()


if __name__ == "__main__":
    # write_proxies()
    get_proxy()
