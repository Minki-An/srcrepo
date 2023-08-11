#!/usr/bin/python

from flask import Flask, render_template, jsonify, session, request, redirect
import json
import requests
import pymysql

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['JSON_AS_ASCII'] = False

order_list='''
[
    {
        "id":"1",
        "name":"맥도날드 햄버거",
        "store":"한국 맥도날드",
        "storeId": "100",
        "price": 8700,
        "img":"https://joinc-edu.s3.ap-northeast-2.amazonaws.com/docker-msa/ham-01.jpeg"
    },
    {
        "id":"2",
        "name":"좋은날 떡복이",
        "store":"좋은음식",
        "storeId": "101",
        "price": 5000,
        "img":"https://joinc-edu.s3.ap-northeast-2.amazonaws.com/docker-msa/tteokbokki.jpeg"
    },
    {
        "id":"3",
        "name":"우리 돈까스",
        "store":"우리돈",
        "storeId": "102",
        "price": 11000,
        "img":"https://joinc-edu.s3.ap-northeast-2.amazonaws.com/docker-msa/pork_cutlet.jpg"
    },
    {
        "id":"4",
        "name":"빅맥 세트",
        "store":"롯데리아",
        "storeId": "103",
        "price": 15000,
        "img":"https://joinc-edu.s3.ap-northeast-2.amazonaws.com/docker-msa/ham-02.jpeg"
    }
]
'''

@app.route("/")
def index():
    username=""
    if "username" in session:
        username=session["username"]

    return render_template(
            "index.html",
            username=username
    )

@app.route("/w/login")
def login():
    if "username" in session:
        return render_template(
            "hello.html",
            username=session["username"]
        )
    else:
        return render_template("login.html")
    

@app.route("/api/order", methods=["GET"])
def products():
    data = json.loads(order_list)
    return jsonify(data)

@app.route("/api/order/<oid>", methods=["GET"])
def order(oid):
    sid="0"
    data = json.loads(order_list)
    for v in data: 
        if v["id"]==oid:
            sid=v["storeId"]
    response = requests.get("/api/store/"+sid)
    store_status = json.loads(response.content)
    return store_status 

@app.route("/api/store/<id>", methods=["GET"])
def store(id):
    store_status={"100":0, "101":1, "102":1, "103":1}
    if id in  store_status.keys():
        data={"status": store_status[id]}
        return jsonify(data) 
    else:
        data={"status": -1}
        return jsonify(data) 

@app.route("/api/user", methods=["POST"])
def login_1():
    session['username'] = request.form['username']
    return redirect("/w/login", code=302)

@app.route("/api/user", methods=["GET"])
def get():
    if "username" in session:
        print(session["username"])
        return ("session found:"+session["username"])
    else:
        return ("Session not found: ")

@app.route("/api/user/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/w/login", code=302)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9000,
        debug=False
    )
