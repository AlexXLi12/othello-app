from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS
from game_state import GameState
app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5000")

# global game state variables
game = GameState()

@app.route('/')
def index():
    global game
    game = GameState()  # reset game state
    return render_template('othello.html')

@app.route('/move', methods=['POST'])
def move_request():
    move = request.args.get('pos' ,'')
    if move:
        move = move[3:]
    print(move)
    is_valid = game.make_move(int(move))
    if not is_valid:
        response_data = {'board': game.board,
                         'to_move': game.to_move,
                         'winner': game.winner,
                         'possible_moves': list(game.possible_moves),
                         'message': 'Invalid move.'}
    else: # move is valid
        response_data = {'board': game.board,
                        'to_move': game.to_move,
                        'winner': game.winner,
                        'possible_moves': list(game.possible_moves),
                        'message': 'Move {} processed.'.format(move)}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)