#!/usr/bin/python3

# Created by Jared Dunbar

from flask import Flask, request, render_template, Response
import string, random, json

app = Flask(__name__)

db = {}

@app.route("/")
def indexAction():
    return render_template("index.html", users=db)

@app.route("/get/<username>")
def getAction(username):
    if username in db:
        resp = json.dumps(db[username])
        return Response(response=resp, mimetype="application/json")
    else:
        return ""

@app.route("/add/<username>/<value>")
def addAction(username, value):
    add(username, value)
    return getAction(username)

@app.route("/del/<username>/<value>")
def delAction(username, value):
    remove(username, value)
    return getAction(username)

def add(username, value):
    if username not in db:
        db[username] = []
    if value not in db[username]:
        db[username].append(value)

def remove(username, value):
    if username in db:
        if value in db[username]:
            db[username].remove(value)

def get(username):
    return db[username]

def clean(inputStr):
    return "".join(
        [c for c in inputStr if c in string.ascii_letters or c in string.whitespace or c in "\\/.,?!|~+=_-[]@#$%^*()"])

def generateSecureKey(size):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

app.secret_key = generateSecureKey(64)

if __name__ == "__main__":
    app.run(debug=True)
