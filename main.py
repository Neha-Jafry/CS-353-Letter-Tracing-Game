# from flask import Flask
import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)

#Add your own details

config = {
    "apiKey": "AIzaSyCAz49LKrO_6XkpF3Qt-uOnsjQNAdqTBtA",
    "authDomain": "se-finalproject.firebaseapp.com",
    "databaseURL": "https://se-finalproject-default-rtdb.firebaseio.com/",
    "projectId": "se-finalproject",
    "storageBucket": "se-finalproject.appspot.com",
    "messagingSenderId": "690862818642",
    "appId": "1:690862818642:web:a4e215155e6054402a668b"
}


#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/game')
def hello():
    print("Hello World")
    return render_template("index.html")

@app.route('/game/score', methods=["POST", "GET"])
def showScore():
    
    print(111)
    score = request.form['score']
    return render_template("score.html")

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/navbar")
def navbar():
    return render_template("nav-bar.html")



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
            #Redirect to welcome page
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
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email, "high score": 0 , "Games Played": 0}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
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


# @app.route('/game')
# def scoreScreen():
#     return render_template('game.html')

@app.route('/scoreScreen')
def scoreScreen():
    return render_template('scoreScreen.html')

if __name__ == "__main__":
    app.run()