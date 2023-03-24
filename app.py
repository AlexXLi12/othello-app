from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5000")

@app.route('/')
def index():
    return render_template('othello.html')

@app.route('/move', methods=['POST'])
def move_request():
    move = request.args.get('pos' ,'')
    if move:
        move = move[3:]
    print(move)
    response_data = {'message': 'Move {} processed.'.format(move)}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)