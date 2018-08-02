import os
import difflib
from flask import Flask, redirect, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'some_secret'



    

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        flash("You are now logged in {} !".format
            (request.form["username"]))
        print(request.form["username"])
    return render_template("ready.html")
    
    

def add_users(username):
    """Add username to the users list """
    print("")
    question = input("Enter your username")
    answer = input("{0}".format(username))
    
    file = open("data/users.txt","a")
    file.write(username + "\n")
    file.close()
    
    

@app.route('/ready')
def ready():
    return render_template("ready.html")
    
    
def answer_riddles(riddle):
    "Play game and answer riddles"
    file = open("data.riddles.txt", "r")
    guess == input(question + "> ")
    if guess == answer:
        score += 1
        print("You're right!")
        print(score)
    else:
        print("You're wrong!")
    
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)