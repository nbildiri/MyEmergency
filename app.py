from google.auth.transport import requests

ACCOUNT_SID = ''
AUTH_TOKEN = ''
FROM_PHONE_NUMBER = ''

from flask import Flask, render_template, request
import json
from twilio.rest import Client

app = Flask(__name__)


@app.route("/")
def mainPage():
    return render_template("main.html")


@app.route("/notifyCall")
def notifyCall():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    pn = request.args.get("phone_number")
    call = client.calls.create(
        twiml='<Response><Say voice="alice" loop="2">Hi! We are calling on behalf of my emergency. we are happy to '
              'have saved you!</Say> <Play>http://demo.twilio.com/docs/classic.mp3</Play></Response>',
        to=pn,
        from_=FROM_PHONE_NUMBER
    )

    ret = {
        "success": True,
        'phone_sent': pn
    }

    connectDB(pn, "call")

    return json.dumps(ret)


@app.route("/notifyText")
def notifyText():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    pn = request.args.get("phone_number")
    message = client.messages.create(
        body='Hi there, Thank you for using *MyEmergency*\nWe are happy to have saved you:) Have an amazing day!',
        to=pn,
        from_=FROM_PHONE_NUMBER
    )

    ret = {
        "success": True,
        "phone_num": pn
    }

    connectDB(pn, "text")

    return json.dumps(ret)


@app.route("/done")
def done():
    return render_template("accomplished.html")


@app.route("/connectDB")
def connectDB(pn, typ):
    import mysql.connector

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
        port='3306',
        database=''
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO user (phone_num, type) VALUES (%s, %s)"
    val = (pn, typ)
    mycursor.execute(sql, val)

    mydb.commit()

    return render_template("accomplished.html")


if __name__ == '__main__':
    app.run()
