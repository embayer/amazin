import json

from flask import Flask, request, render_template, jsonify
import couchdb


app = Flask(__name__)
CDB_URL = 'http://127.0.0.1:5984/'
couch = couchdb.Server(CDB_URL)
product_db = couch['products']
keyword_db = couch['keywords']

DATA_FILE = 'data/data.json'


def dump_keyword(data):
    keyword = data['field-keywords']
    if keyword not in keyword_db:
        # create
        keyword_db.save(data)
    else:
        # update
        doc = keyword_db[keyword]
        for key, value in data.items():
            doc[key] = value
        keyword_db[doc.id] = doc

def dump_product(data):
    asin = data['asin']
    if asin not in product_db:
        # create
        product_db.save(data)
    else:
        # update
        doc = product_db[asin]
        for key, value in data.items():
            doc[key] = value
        product_db[doc.id] = doc
    with open(DATA_FILE, 'a+') as outfile:
        json.dump(data, outfile)
        outfile.write('\n')


@app.route('/')
def show_data():
    data = {'results': []}
    with open(DATA_FILE, 'r') as f:
        for line in f:
            data['results'].append(json.loads(line))

    return jsonify(data)


@app.route('/bookmarklet')
def show_bookmarklet():
    minified = ''
    with open('bookmarklet.js', 'r') as infile:
        for line in infile:
            minified = '{}{}'.format(minified, line.replace('\n', ''))
    return render_template('bookmarklet.html', href=minified)


@app.route('/post', methods=['GET', 'POST'])
def post_product():
    data = {}
    for a in request.args:
        data[a] = request.args[a]
    if data['type'] == 'product':
        dump_product(data)
    elif data['type'] == 'keyword':
        dump_keyword(data)

    return render_template('success.html')


if __name__ == '__main__':
    app.run()
