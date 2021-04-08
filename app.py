from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth


app = Flask(__name__)
app.config["TESTING"] = True

config = {
    "apiKey": "AIzaSyBG22gTgUR61Ek_7CigmTQNGGcASGQEQSI",
    "authDomain": "cblite-e2c13.firebaseapp.com",
    "databaseURL": "https://cblite-e2c13-default-rtdb.firebaseio.com",
    "projectId": "cblite-e2c13",
    "storageBucket": "cblite-e2c13.appspot.com",
    "messagingSenderId": "322571040642",
    "appId": "1:322571040642:web:f708bdfa998ce0f096c19b"
}
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
#Connect to firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")


#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to chooseGame page
            return redirect(url_for('chooseGame'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('chooseGame'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            print("here \n")
            auth.create_user_with_email_and_password(email, password)
            print("here1 \n")
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            print("here2 \n")
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            print("here3 \n")
            db.child("users").child(person["uid"]).set(data)
            #Go to chooseGame page
            return redirect(url_for('chooseGame'))
        except:
            #If there is any error, redirect to register
                
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('chooseGame'))
        else:
            return redirect(url_for('register'))


@app.route('/chooseGame')
def chooseGame():
    if person["is_logged_in"] == True:
        return render_template("chooseGame.html", name = person["name"])
    else:
        return redirect(url_for('login'))


# @app.route('/Game')
# def scoreScreen():
#     return render_template('Game.html')

@app.route('/scoreScreen')
def scoreScreen():
    return render_template('scoreScreen.html')

if __name__ == '__main__':
    app.run(debug=True)