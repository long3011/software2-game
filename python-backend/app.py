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
@app.route('/mainScreen/<option>')
def main_screen(option):
    if option=='leaderboard':       #view the leaderboard
        return jsonify({'status':'leaderboard','content':view_leaderboard()})
    elif option=='personal':        #view the personal saves
        return jsonify({'status':'personal','content':personal_load()})
@app.route('/loadSave/<id>',methods=['POST'])
def load_save(player_id):   #load the selected saves
    global player
    player=saves_load(personal_load()[int(player_id)])
    return jsonify({
        'name': player.information()[0],
        'difficulty': player.information()[1],
        'money': player.information()[2],
        'airports': player.information()[3],
        'fuel': player.information()[5],
        'hints': player.information()[6],
        'co2': player.information()[7],
        'points': player.calculate_points(),
    })
@app.route('/loadLeaderboard/<name>/<difficulty>/<id>',methods=['PUT'])
def load_leaderboard(name,difficulty,player_id):    #load the selected leaderboard item with name and difficulty input
    global player
    global leaderboard
    global used_seed
    leaderboard=True
    used_seed=view_leaderboard()[int(player_id)-1][3]
    ap_list=leaderboard_load(view_leaderboard()[int(player_id)-1][2].split(','))
    player=Player(name,difficulty,1000*(4-int(difficulty)),ap_list)
    return jsonify({
        'name': player.information()[0],
        'difficulty': player.information()[1],
        'money': player.information()[2],
        'airports': player.information()[3],
        'fuel': player.information()[5],
        'hints': player.information()[6],
        'co2': player.information()[7],
        'points': player.calculate_points(),
    })
@app.route('/mainGame/<name>/<difficulty>')
def main_game(name,difficulty):     #start the main game without loading previous saves
    global player
    player=Player(name,int(difficulty),1000*(4-int(difficulty)),airports(12))
    return jsonify({
        'name':player.information()[0],
        'difficulty':player.information()[1],
        'money':player.information()[2],
        'airports':player.information()[3],
        'fuel':player.information()[5],
        'hints':player.information()[6],
        'co2':player.information()[7],
        'points':player.calculate_points(),
    })
@app.route('/flyTo/<airport_id>')
def fly_to(airport_id):     #innitiate flying to airport, id refer to key of airport inside dictionary
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
    return jsonify(packet)
@app.route('/shop/<item>')
def shop(item):     #let player buy hints or fuel
    global player
    if item=='hints':
        player.buy_hints()
    elif item=='fuel':
        player.buy_fuel()
    return jsonify({
        'balance':player.show_balance()
    })
@app.route('/hint')
def hint():     #give player hints about the closest airport
    global player
    nearest_airport={
        'nearest':player.use_hint()[0]
    }
    return jsonify(nearest_airport)

@app.route('/quit/<status>')
def game_stop(status): #status have 2 states, saving to leaderboard or saving to personal progress
    global player
    global leaderboard
    global used_seed
    stop_status=None
    if status=='leaderboard':
        if leaderboard:
            stop_status=leaderboard_save_used(player,used_seed)
        else:
            stop_status=leaderboard_save(player)
    elif status=='personal':
        stop_status = personal_save(player)
    return jsonify({'status':stop_status})
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=8000)