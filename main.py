#!/usr/bin/python3

# Created by Jared Dunbar

from flask import Flask, request, render_template, Response
import string, random, json, os.path, threading, time

app = Flask(__name__)

db = {}

DATABASE_FILE = "signals.db"
IP_WHITELIST = ["127.0.0.1", "128.153.145.150", "128.153.145.151"]
PREFIX = "/signals"

def save():
    try:
        f = open(DATABASE_FILE, "w")
        data = json.dumps(db)
        f.write(data)
        f.close()
    except:
        print("[Error] Unable to write to database file {}".format(DATABASE_FILE))

if os.path.isfile(DATABASE_FILE):
    try:
        f = open(DATABASE_FILE)
        data = f.readlines()[0]
        f.close()
        db = json.loads(data)
        print("Database Loaded")
    except:
        print("[Error] Unable to read from database file {}".format(DATABASE_FILE))

@app.route("{}/".format(PREFIX))
def indexAction():
    return render_template("index.html", users=db)

@app.route("{}/getall".format(PREFIX))
def getAllAction():
    resp = json.dumps(db)
    return Response(response=resp, mimetype="application/json")

@app.route("{}/get/<username>".format(PREFIX))
def getAction(username):
    if username in db:
        resp = json.dumps(db[username])
        return Response(response=resp, mimetype="application/json")
    else:
        return Response(response="{}", mimetype="application/json")

@app.route("{}/add/<username>/<value>".format(PREFIX))
def addAction(username, value):
    if len(IP_WHITELIST) > 0:
        if request.remote_addr in IP_WHITELIST:
            add(username, value)
            return getAction(username)
        else:
            return getAction(username)
    else:
        add(username, value)
        return getAction(username)

@app.route("{}/del/<username>/<value>".format(PREFIX))
def delAction(username, value):
    if len(IP_WHITELIST) > 0:
        if request.remote_addr in IP_WHITELIST:
            remove(username, value)
            return getAction(username)
        else:
            return getAction(username)
    else:
        remove(username, value)
        return getAction(username)

def add(username, value):
    if username not in db:
        db[username] = []
    if value not in db[username]:
        db[username].append(value)
        save()

def remove(username, value):
    if username in db:
        if value in db[username]:
            db[username].remove(value)
            save()

def get(username):
    return db[username]

def clean(inputStr):
    return "".join(
        [c for c in inputStr if c in string.ascii_letters or c in string.whitespace or c in "\\/.,?!|~+=_-[]@#$%^*()"])

def generateSecureKey(size):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

app.secret_key = generateSecureKey(64)

if __name__ == "__main__":
    app.run()
