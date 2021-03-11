from flask import Flask, render_template

app = Flask(__name__)
app.config["TESTING"] = True

@app.route('/')
def index():
    return render_template('index.html')
    # return("Hello World!")

@app.route('/chooseGame')
def chooseGame():
    return render_template('chooseGame.html')

@app.route('/scoreScreen')
def scoreScreen():
    return render_template('scoreScreen.html')