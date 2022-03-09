from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    retval = [{ "message": "Hello, World!" }]
    return jsonify(retval)
