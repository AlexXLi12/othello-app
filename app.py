import time
from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS
from game_state import GameState
from othello import engine
app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5000")

# global game state variables
global game

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_game', methods=['POST'])
def create_game_obj():
    global game
    depth_limit = request.form.get('engine_depth', '6')
    time_limit = request.form.get('time_limit', '2')
    depth_limit = int(depth_limit)
    time_limit = float(time_limit)
    print(depth_limit, time_limit)
    game = GameState(depth_limit, time_limit)  # reset game state
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
    startTime = time.time()
    move = engine.calc_move(game.board, game.to_move, game.engine_depth, game.engine_time)
    total_time = time.time() - startTime
    if move != -1:
        game.make_move(move, engine=True)
        response_data = {'board': game.board,
                    'to_move': game.to_move,
                    'winner': game.winner,
                    'possible_moves': list(game.possible_moves),
                    'message': 'Engine moved to {}.'.format(move),
                    'time': total_time}
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
    depth_limit = game.engine_depth
    time_limit = game.engine_time
    game = GameState(depth_limit, time_limit)  # reset game state
    response_data = {'board': game.board,
                     'to_move': game.to_move,
                     'winner': game.winner,
                     'possible_moves': list(game.possible_moves),
                     'message': 'Game reset.'}
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)