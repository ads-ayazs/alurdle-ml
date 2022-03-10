from flask import Flask, jsonify
from routes.validate_word import blueprint as bp_validate_word
# import validate_word

app = Flask(__name__)
app.register_blueprint(bp_validate_word)


@app.route("/")
def hello_world():
    retval = [{ "message": "Hello, World!" }]
    return jsonify(retval)

if __name__ == "__main__":
    app.run()
