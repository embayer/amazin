from subprocess import call
import json

from flask import Flask, request, render_template, jsonify
import couchdb


app = Flask(__name__)
CDB_URL = 'http://127.0.0.1:5984/'
couch = couchdb.Server(CDB_URL)
db = couch['products']

DATA_FILE = 'data/data.json'


def dump(data):
    db.save(data)
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
def post_link():
    data = {}
    for a in request.args:
        data[a] = request.args[a]
    dump(data)

    return render_template('success.html')


if __name__ == '__main__':
    app.run()
