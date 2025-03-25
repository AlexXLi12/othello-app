from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS
from game_state import GameState
from othello import engine
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
    if game.to_move != 'X':
        return jsonify({'board': game.board,
                        'to_move': game.to_move,
                        'winner': game.winner,
                        'possible_moves': list(game.possible_moves),
                        'message': "Not player's move"})
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

@app.route('/engine', methods=['GET'])
def get_engine_move():
    if game.to_move != 'O':
        return jsonify({'board': game.board,
                        'to_move': game.to_move,
                        'winner': game.winner,
                        'possible_moves': list(game.possible_moves),
                        'message': "Not engine's move"})
    move = engine.calc_move(game.board, game.to_move)
    if move != -1:
        game.make_move(move, engine=True)
        response_data = {'board': game.board,
                    'to_move': game.to_move,
                    'winner': game.winner,
                    'possible_moves': list(game.possible_moves),
                    'message': 'Engine moved to {}.'.format(move)}
    else:
        # engine has no valid moves; give turn to player
        response_data = {'board': game.board,
                    'to_move': game.to_move,
                    'winner': game.winner,
                    'possible_moves': list(game.possible_moves),
                    'message': 'Engine has no valid moves.'}
    return jsonify(response_data)


@app.route('/state', methods=['GET'])
def get_state():
    response_data = {'board': game.board,
                     'to_move': game.to_move,
                     'winner': game.winner,
                     'possible_moves': list(game.possible_moves)}
    return jsonify(response_data)

@app.route('/reset', methods=['POST'])
def reset_game():
    global game
    game = GameState()
    response_data = {'board': game.board,
                     'to_move': game.to_move,
                     'winner': game.winner,
                     'possible_moves': list(game.possible_moves),
                     'message': 'Game reset.'}
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)