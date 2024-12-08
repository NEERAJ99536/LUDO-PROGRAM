from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

players = []
scores = {}
current_player = 0  # Tracks whose turn it is
dice_img = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    global players, scores, current_player, dice_img
    if request.method == 'POST':
        players = [request.form.get(f'player{i}') for i in range(1, 5)]
        scores = {player: 0 for player in players}
        current_player = 0
        dice_img = "/static/dice1.png"
        return redirect(url_for('game'))

    return render_template('index.html')

@app.route('/game')
def game():
    global players, scores, current_player, dice_img
    return render_template('game.html', players=players, scores=scores, dice_img=dice_img, current_player=players[current_player])

@app.route('/roll_dice')
def roll_dice():
    global players, scores, current_player, dice_img
    dice = random.randint(1, 6)
    dice_img = f"/static/dice{dice}.png"
    
    scores[players[current_player]] += dice
    current_player = (current_player + 1) % len(players)
    
    return redirect(url_for('game'))

@app.route('/winner')
def winner():
    global scores
    ranked_players = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return render_template('winner.html', ranked_players=ranked_players)

if __name__ == '__main__':
    app.run(debug=True)
