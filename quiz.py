import os
import json
import copy
from flask import Flask, flash, session, redirect, render_template, request, flash
from collections import Counter


app = Flask(__name__)
app.secret_key = 'some_secret'



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
    write_file("quiz/data/users.txt", username)
 
 
"""
Get all incorrect answers
"""
def get_all_incorrect_answers():
    answers = []
    with open("quiz/data/incorrect_answers.txt", "r") as incorrect_answers:
        users = [row for row in incorrect_answers]
        return answers[-7:]  
        

"""
Get all online users
"""
def get_all_online_users():
    users = []
    with open("quiz/data/users.txt", "r") as online_users:
        users = [row for row in online_users]
        return users[-7:] 


# Function to add a player's score to the leaderboard
def add_to_scoreboard(username, final_score):
    leaders = get_leaders()
    with open("quiz/data/scores.txt", "a") as scoreboard:
        if not (username, final_score) in leaders:
            scoreboard.write('\n{}:{}'.format(str(username), str(final_score)))
    
 
# Function to get top 10 leaders
def get_leaders():
    with open("quiz/data/scores.txt") as leaders:
        leaders = [line for line in leaders.readlines()[1:]]
        sorted_leaders = []
        for leader in leaders:
            tupe = (leader.split(':')[0].strip(), int(leader.split(':')[1].strip()))
            sorted_leaders.append(tupe)
            
        # Sort leaders and display top 10
        return sorted(sorted_leaders, key=lambda x: x[1], reverse = True)[:10]


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Welcome page, add username.
    """
    if request.method == "POST":
        new_user(request.form["username"])
        session['username'] = request.form['username']
        session['index'] = 0
        session['attempts'] = 0
        session['riddle'] = 0
        session['score'] = 0
        return redirect(request.form["username"])
    return render_template("index.html")
    

@app.route("/<username>", methods = ["GET","POST"]) #Username passed from index function, value optained from form post. 
def riddle(username):
    #Load the json file containing the riddles
    riddles = []
    with open("quiz/data/riddles.json", "r") as riddle_data:
        riddles = json.load(riddle_data)	
    
    if request.method == "POST":
        print(session['index'])
        print(session['score'])
        print(request.form['answer'])
        if session['index'] <= 4:
            user_answer = request.form["answer"]
            print(user_answer)
            if riddles[session['index']]["answer"] == user_answer:
                session['score'] += 1
                session['index'] += 1
                flash('You have got it right!')
                print(session['attempts'])
                print(session['score'])
            else:
                session['attempts'] += 1
        else:
            session.pop('_flashes', None) # Return None to avoid Error on the last riddle
            
    
    # Return final score and add player to scoreboard
    add_to_scoreboard(username, session['score'])
    return render_template('scores.html', final_score=session('score'), leaders=get_leaders())
    
# Display for the scoreboard
@app.route('/leaders')
def leaders():
    leaders = get_leaders()
    return render_template("scores.html", leaders=leaders)
	        
 
 
    # To end the game after 3 incorrect answers
    if session['attempts'] >= 3:
            write_file("quiz/data/scores.txt", "{0}" " ({1})" .format(session['score'], session['username']))
            return redirect("game_over")		    
		    

    
    
    incorrect_answers = get_all_incorrect_answers()
    
    context = {
        'riddle_question': session['riddle'],
        'index': session['index'],
        'attempts': session['attempts'],
        'incorrect_answers': incorrect_answers,
        'username': session['username'],
        'score': session['score']
    }
    
    return render_template("ready.html", context=context)
	
	
@app.route("/game_over", methods = ["GET","POST"])
def game_over():
	
	scores = session('score')()
			
	return render_template("game_over.html", scores = scores)


if __name__ == '__main__':
	app.run(host=os.environ.get("IP"),
		port=int(os.environ.get("PORT")), 
		debug=True)