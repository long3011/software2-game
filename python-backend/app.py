from flask import Flask,jsonify
from flask_cors import CORS
from airport import airports
from player import Player
from saving import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

player=None
leaderboard=False
used_seed=None
@app.route('/<option>')
def main_screen(option):
    if option=='leaderboard':
        return view_leaderboard()
    elif option=='play':
        return personal_load()
@app.route('/loadSave/<id>',methods=['POST'])
def load_save(player_id):
    global player
    player=saves_load(personal_load()[int(player_id)])
@app.route('/loadLeaderboard/<name>/<difficulty>/<id>',methods=['POST'])
def load_leaderboard(name,difficulty,player_id):
    global player
    global leaderboard
    global used_seed
    leaderboard=True
    used_seed=view_leaderboard()[int(player_id)-1][3]
    ap_list=leaderboard_load(view_leaderboard()[int(player_id)-1][2].split(','))
    player=Player(name,difficulty,1000*(4-int(difficulty)),ap_list)
@app.route('/mainGame/<name>/<difficulty>',methods=['POST'])
def main_game(name,difficulty):
    global player
    player=Player(name,difficulty,1000*(4-int(difficulty)),airports(12))
@app.route('/flyTo/<destination>/',methods=['POST'])
def fly_to(airport_id):
    global player
    distance=player.fly(airport_id)
    points=player.calculate_points()
    remaining=player.remaining_airports()
    fuel=player.fuel_left()
    packet={
        'distance':distance,
        'points':points,
        'remaining':remaining,
        'fuel':fuel,
    }
    return packet
@app.route('/shop/<item>/',methods=['POST'])
def shop(item):
    global player
    if item=='hints':
        player.buy_hints()
    elif item=='fuel':
        player.buy_fuel()
    return {'balance':player.show_balance()}
@app.route('/hint',methods=['GET'])
def hint():
    global player
    nearest_airport={'nearest':player.use_hint()[0]}
    return nearest_airport

@app.route('/quit/<status>/',methods=['POST'])
def game_stop(status): #status have 2 states, saving to leaderboard or saving to personal progress
    global player
    global leaderboard
    global used_seed
    if status=='leaderboard':
        if leaderboard:
            status=leaderboard_save_used(player,used_seed)
        else:
            status=leaderboard_save(player)
        return {'status':status}
    elif status=='personal':
        status = personal_save(player)
        return {'status': status}
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=8000)