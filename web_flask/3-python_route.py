#!/usr/bin/python3
"""
A script that starts a Flask web application
"""
from flask import Flask
from sys import argv

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def display_c(text):
    return f"C {text.replace('_', ' ')}"


@app.route("/python", defaults={'text': "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def display_py(text):
    return f"Python {text.replace('_', ' ')}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
