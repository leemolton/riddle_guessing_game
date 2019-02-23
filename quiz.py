import os
import json
import copy
from flask import Flask, render_template, request, flash, redirect, session, url_for
from collections import Counter

app = Flask(__name__)
app.secret_key = 'some_secret'


MAX_ATTEMPTS = 3
with open("quiz/data/riddles.json", "r") as json_data:
    riddles = json.load(json_data)
    print(riddles)


high_score = {
    "name": "nobody",
    "score": 0
}


"""
Welcome page, add username and initialize with default values.
"""
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_user(request.form["username"])
        session['username'] = request.form['username']
        return redirect(request.form['username'])
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


@app.route("/new_game", methods=["POST"])
def new_game():
    session['username'] = request.form['username']
    session['index'] = 0
    session['score'] = 0
    session['riddle_num'] = 0
    session['attempts'] = MAX_ATTEMPTS
    return redirect(url_for("riddle"))


"""
Load the json file containing the riddles
"""
@app.route("/<username>", methods = ["GET","POST"]) #Username passed from index function, value optained from form post. 
def riddle(username):
    if "username" not in session:
        return redirect(url_for("index"))
      
    if request.method == "POST" and session['riddle_num'] < len(riddles):
        previous_riddle = riddles[session['riddle_num']]
        if request.form['answer'].lower() == previous_riddle["answer"]:
            session['score'] += 1 # increments the score if the answer is correct
            #session['index'] += 1 # increments the index to the next question if the answer is correct
            session['riddle_num'] += 1
            print('answer')
            print(session['riddle_num'])
            if session['riddle_num'] < len(riddles):
                flash('You have got it right!')
                print('You have got it right!')
                print(session['index'])
                print(session['riddle'])
                print(session['riddle_num'])
            else:
                flash("Correct answer, %s!" % session['username'])
        elif not session['attempts']:
            session['riddle_num'] += 1
            session['attempts'] = MAX_ATTEMPTS
            if session['riddle_num'] < len(riddles):
                flash("Wrong answer, try again!")
        else:
            session['attempts'] = 1
            flash("Wrong answer, %s. You have %s attempts left." % (
                  session['username'], session['attempts']))
                  
    if session["riddle_num"] >= len(riddles):
        if session['score'] >= high_score['score']:
            high_score['score'] = session['score']
            high_score['username'] = session['username']
        return render_template("game_over.html", username=session['username'],
                        score=session['score'],
                        highscore=high_score['score'],
                        highscorer=high_score['username'])
    
    context = {
        'index': session['index'],
        'question': session['question'],
        'attempts': session['attempts'],
        'username': session['username'],
        'score': session['score']
        }
        
    new_riddle = riddles[session['riddle_num']]
    return render_template("ready.html", riddle=new_riddle['riddle'], riddleNumber=session['riddle_num'], context=context)
        
        
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