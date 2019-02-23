import os
import json
import copy
from flask import Flask, render_template, request, flash, redirect, session
from collections import Counter

app = Flask(__name__)
app.secret_key = 'some_secret'


"""
Welcome page, add username and initialize with default values.
"""
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_user(request.form["username"])
        session['username'] = request.form['username']
        return redirect(request.form["username"])
    return render_template("index.html")


"""
Opening a file and writing to it
"""
def write_file(filename, message):
    with open (filename, 'a') as file:
        file.writelines(message + "\n")


"""
Add new users to the users file
"""
def new_user(username):
    write_file("quiz/data/users.txt", username)


"""
Count the number of riddles in our list and we can keep score.
"""
def countRiddles():
    numRiddles = len(loadRiddles)
    return numRiddles


"""
Load the json file containing the riddles
"""
def loadRiddles():
    riddles = []
    #Load the json file containing the riddles
    with open("quiz/data/riddles.json", "r") as json_data:
        riddles = json.load(json_data)
        print(riddles)
        return riddles
        

@app.route("/<username>", methods = ["GET","POST"])
def new_game(username):
    #Set the index to 0 to display the first riddle in the list 
    session['index'] = 0
    session['score'] = 0
    session['attempts'] = 0
    
    # riddles are stored in JSON file and are indexed
    riddles = []
    
    # Load JSON data from riddles.json
    riddles = loadRiddles()
    
    # Set the first riddle
    session['questionNumber'] = 0
        
    if request.method == "POST":
        print(session['index'])
        if session['index'] <= 4:
        
        # post riddle number and increment the riddle by 1 each time 
        # a correct answer is given.
            user_answer = request.form['answer']
            actual_answer = riddles[session['index']]['answer']
            print(user_answer)
            session['score'] += 1 
            session['questionNumber'] += 1 
            flash('You have got it right!')
            print('You have got it right!')
            session['index'] += 1 
            print(session['index'])
            print(session['attempts'])
            print(session['score'])
            print(session['questionNumber'])
            print(question)
        else:
            session['attempts'] += 1
    else:
            session.pop('_flashes', None) # Return None to avoid an Error on the last riddle
    
    context = {
        'index': session['index'],
        'question': session['question'],
        'questionNumber': session['questionNumber'],
        'attempts': session['attempts'],
        'username': session['username'],
        'score': session['score']
        }
        
    return render_template("ready.html", question=session['question'], username=username, context=context)
    
            
    # To end the game after 3 incorrect answers
@app.route("/game_over", methods = ["GET","POST"])
def game_over():
    if session['attempts'] <= 3:
        write_file("quiz/data/scores.txt", "{0}" " ({1})" .format(session['score'], session['username']))
        return redirect("game_over")
        
        
"""
Get players score and add player to scoreboard
"""
@app.route('/leaders')
def leaders(username, final_score):
    leaders = get_leaders()
    

# Function to add a player's score to the leaderboard
def add_to_scoreboard(username, final_score):
    leaders = get_leaders()
    with open("quiz/data/scores.txt", "a") as scoreboard:
        if not (username, final_score) in leaders:
            scoreboard.write('\n{}:{}'.format(str(username), str(final_score)))
    return render_template('scores.html', final_score = (session['score']), leaders = get_leaders())
  
    
"""
Get top 10 leaders
"""
def get_leaders():
    with open("quiz/data/scores.txt") as leaders:
        leaders = [line for line in leaders.readlines()[1:]]
        sorted_leaders = []
        for leader in leaders:
            tupe = (leader.split(':')[0].strip()) # ('lee', 5)
            sorted_leaders.append(tupe)
            
        # Sort leaders and display top 10
        return sorted(sorted_leaders, key=lambda x: x[:1], reverse = True)[:10]


if __name__ == '__main__':
	app.run(host=os.environ.get("IP"),
		port=int(os.environ.get("PORT")), 
		debug=True)