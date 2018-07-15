import os
import json
from flask import Flask, redirect, request, render_template



app = Flask(__name__)
app.secret_key = "secret"


"""
Get all incorrect_answers():
"""
def get_all_incorrect_answers():
	answers = []
	with open("data/incorrect_answers.txt", "r") as incorrect_answers:
			answers = [row for row in incorrect_answers]
			return answers
			

"""
Get all online_users():
"""
def get_all_online_users():
    users = []
    with open("data/users.txt", "r") as online_users:
                users = [row for row in online_users]
                return users


"""
Reusable function for opening a file and writing to it
"""
def write_file(filename, message):
	with open (filename, 'a') as file:
		file.writelines(message + "\n")


"""
Add new users to the users file
"""
def new_user(username):
    write_file("data.users.txt", username)
    

@app.route("/", methods =["GET", "POST"])
def index():
    """
    Welcome page, add username.
    """
    if request.method == "POST":
        new_user(request.form["username"])
        return redirect(request.form["username"])
    return render_template("index.html")
    

@app.route("/<username>", methods = ["GET","POST"]) #Username passed from index function, value optained from form post.     
def riddle(username):
    #Load the riddle file containing the riddles
    riddles = []
    with open("data/riddles.txt", "r") as riddle_data:
        riddles = txt.read(riddle_data)
        #Set the index to 0 to display the first riddle in the list first
        index = 0
    
    
        if request.method == "POST":
            index = int(request.form["index"])  #Specify index to be an integer not a string or else will return a type error
            user_answer = request.form["answer"].lower()
            if riddles[index]["answer"] == user_answer:
                index +=1
                write_file("data/correct_answers.txt", "{0}" "({1})" .format(user_answer, username))
            else:
                write_file("data/incorrect_answers.txt", "{0}" "{1})" .format(user_answer, username))
            
    
        if request.method == "POST":
            if user_answer == "palmtree" and index >= 7:
                return redirect("game_over")
            
    
    incorrect_answers = get_all_incorrect_answers()
    online_users = get_all_online_users()
    
    
    return render_template("riddles.html", riddle_question = riddles, index = index, online_users = online_users, incorrect_answers = incorrect_answers, username = username)
    

@app.route("/game_over", methods = ["GET","POST"])
def game_over():
	answers = []
	with open("data/correct_answers.txt", "r") as correct_answers:
		answers = [row for row in correct_answers]
	
		
	return render_template("game_over.html", answers = answers)


if __name__ == '__main__':
	app.run(host=os.environ.get("IP"),
		port=int(os.environ.get("PORT")), 
		debug=True)