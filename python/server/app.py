from flask import Flask, jsonify, request
from python.data import players_by_team
app = Flask(__name__)

@app.route('/players', methods=['GET'])
def get_players():
    team_1 = request.args.get('team1')
    team_2 = request.args.get('team2')
    data = players_by_team.get_dict()
    response = jsonify({team_1: data.get(team_1), team_2: data.get(team_2)})
    response.charset = "utf-8"
    return response.data.decode('utf-8')

# @app.route('/players', methods=['POST'])
# def add_player():
#     new_player = request.json
#     data['players'].append(new_player)
#     return jsonify({'message': 'Player added successfully', 'player': new_player}), 201

if __name__ == '__main__':
    app.run(debug=True)
