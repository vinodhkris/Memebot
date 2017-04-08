#!flask/bin/python
from flask import Flask
from flask import request
from db import MongoObj

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/main/api/v1.0/memes', methods=['GET'])
def getMemes():
    text = request.args.get('text')
    actor = request.args.get('actor')
    m = MongoObj()
    return m.find_doc(text,actor)

@app.route('/main/api/v1.0/memes/size', methods=['GET'])
def getNumberOfMemes():
    m = MongoObj()
    return m.number_of_docs()

if __name__ == '__main__':
    app.run(debug=True)
