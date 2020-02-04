from flask import Flask, render_template, request,abort,Response,jsonify
import requests
app = Flask(__name__)
import csv
import sqlite3
import json
import datetime
import time 
import logging

@app.route('/')
def homepage():
    con = sqlite3.connect("self_healing.db")
    cur = con.cursor()
    shows={}
    query="SELECT name FROM shows  ORDER BY rating DESC LIMIT 5;"
    cur.execute(query,)
    shows=cur.fetchall()
    cur.close()
    if not shows:
        return Response(204)
    return json.dumps(shows),200

@app.route('/adduser', methods=['POST'])
def adduser():
    if request.method=='POST':
        req=request.get_json()
        name = req['username']
        password = req['password']
        con = sqlite3.connect("self_healing.db")
        cur = con.cursor()
        query='SELECT password FROM user WHERE username =?;'
        cur.execute(query,(name,))   
        passw = cur.fetchall()
        if len(passw)==0:
                query='INSERT INTO user (username, password) VALUES (?,?);'
                cur.execute(query, (name, password,))
                con.commit()
                cur.close()
                return Response(status=201)
        else:
                return abort(400)
    
@app.route('/addreview' , methods=['POST'])
def review():
    if request.method=='POST':
        req=request.get_json()
        name = req['username']
        show = req['show']
        review=req['review']
        con = sqlite3.connect("self_healing.db")
        cur = con.cursor()
        query='select username from user where username=?;'
        cur.execute(query,(name,))   
        count = cur.fetchall()
        if(count==0):
            print("user doesn't exist")
            return abort(400)
        query='select name from shows where name=?;'
        cur.execute(query,(show,))   
        count = cur.fetchall()
        if(count==0):
            print("Show doesn't exist")
            return abort(400)
        query='SELECT count(*) FROM review;'
        cur.execute(query,)   
        count = cur.fetchall()
        if(count==0):
            query='INSERT into review(id,name,show,review,upvote,downvote) values (1,?,?,?,0,0);'
            cur.execute(query,(name,review,show,))
            con.commit()
            cur.close()
            return Response(status=201)
        else:
            query="SELECT id FROM review ORDER BY id DESC LIMIT 1;"
            cur.execute(query,)   
            primary_key = cur.fetchall()
            query='INSERT into review(id,name,show,review,upvote,downvote) values (1,?,?,?,0,0);'
            cur.execute(query,(name,review,show,))
            con.commit()
            cur.close()
            return Response(status=201)

@app.route('/listreviews',methods=['GET'])
def listreview():
    if request.method=='GET':
        con = sqlite3.connect("self_healing.db")
        cur = con.cursor()
        query='SELECT * from review;'
        cur.execute(query,)
        coun=cur.fetchall()
        return json.dumps(coun),200
      
@app.route('/listreviews/<review_id>/upvote', methods=['POST'])
def upvote(review_id):
    if request.method=='POST':
        con = sqlite3.connect("self_healing.db")
        cur = con.cursor()
        query='update review set upvote=upvote+1 where id=?;'
        cur.execute(query,(review_id,))
        coun=cur.fetchall()
        con.commit()
        cur.close()
        return json.dumps(coun),200
    
@app.route('/listreviews/<review_id>/downvote', methods=['POST'])
def downvote(review_id):
    if request.method=='POST':
        con = sqlite3.connect("self_healing.db")
        cur = con.cursor()
        query='update review set downvote=downvote+1 where id=?;'
        cur.execute(query,(review_id,))
        coun=cur.fetchall()
        con.commit()
        cur.close()
        return json.dumps(coun),200            

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True, port=8000)
