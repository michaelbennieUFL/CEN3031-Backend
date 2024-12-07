from flask import Blueprint, jsonify, make_response, request
from Extensions import DATABASE as db
from DataModels import Match

data_bp = Blueprint("data", __name__, url_prefix="/data")

@data_bp.route('/games', methods=['GET', 'OPTIONS'])
def get_games():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    matches = Match.query.all()
    games_list = []
    for m in matches:
        games_list.append({
            'id': m.id,
            'date': m.date.strftime('%Y-%m-%d'),
            'team1': m.team1.name if m.team1 else None,
            'team2': m.team2.name if m.team2 else None,
            'team1_goals': m.team1_goals,
            'team2_goals': m.team2_goals,
            'winner_team': m.winner_team.name if m.winner_team else 'none',
            'team1_saves': m.team1_saves,
            'team2_saves': m.team2_saves
        })

    response = jsonify(games_list)
    response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200
