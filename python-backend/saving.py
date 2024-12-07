import os
import json
from airport import connection
import mysql.connector
from player import Player
from airport import Airport

def personal_save(obj):
    try:
        arr=obj.information()
        if os.stat("save.json").st_size != 0:
            with open('save.json') as f:
                info_save = json.load(f)
        else:
            info_save = {}
        info_save[len(info_save)+1]=arr
        with open('save.json', 'w') as f:
            json.dump(info_save, f)
        return "success"
    except FileNotFoundError:
        open('save.json', 'x')
        return personal_save(obj)
def personal_load():
    try:
        if os.stat("save.json").st_size != 0:
            with open('save.json') as f:
                info = json.load(f)
            return info
        else:
            return "There is no saves yet"
    except FileNotFoundError as e:
        return e
def saves_load(result):
    ap_list = {}
    ap_travelled = {}
    for i in result[3]:
        things=result[3][i]
        ap_list[i]=Airport(things[0], things[1], things[2], things[3], things[4], things[5], things[6])
    for i in result[4]:
        things = result[4][i]
        ap_travelled[i]=Airport(things[0], things[1], things[2], things[3], things[4], things[5], things[6])
    info = Player(result[0], result[1], result[2], ap_list, ap_travelled, result[5], result[6], result[7])
    return info
def leaderboard_save(info):
    try:
        stuff=info.leaderboard()
        player_name=stuff[0]
        airport_save=stuff[1]
        player_score=stuff[2]
        cursor = connection.cursor()
        sql_save = (f"INSERT INTO list_airport (airport_list) VALUES ('{airport_save}');")
        cursor.execute(sql_save)  # saving player information into database
        sql_save = (f"INSERT INTO player (NAME,score,airport_seed) VALUES ('{player_name}',{player_score},LAST_INSERT_ID());")
        cursor.execute(sql_save)  # splitting the saving command into 2 because database is funky
        return "success"
    except mysql.connector.errors.DatabaseError as e:
        return e
def leaderboard_save_used(info,player_use_seed):
    try:
        stuff=info.leaderboard()
        player_name=stuff[0]
        player_score=stuff[2]
        cursor = connection.cursor()
        sql_save = (f"INSERT INTO player (NAME,score,airport_seed) VALUES ('{player_name}',{player_score},{player_use_seed});")
        cursor.execute(sql_save)  # saving player information into database
        return "success"
    except mysql.connector.errors.DatabaseError as e:
        return e
def view_leaderboard():
    try:
        cursor = connection.cursor()
        player_fetch = (f"SELECT player.name,player.score,list_airport.airport_list,list_airport.list_seed "
                        f"FROM player, list_airport "
                        f"WHERE player.airport_seed=list_airport.list_seed ")
        cursor.execute(player_fetch)
        output = cursor.fetchall()
        if cursor.rowcount > 0:
            return output
        else:
            return ["There is no leaderboard information"]
    except mysql.connector.errors.DatabaseError as e:
        return {"output":e}
def leaderboard_load(list_ident):
    try:
        airport_list = {}
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT airport.ident, airport.NAME, airport.type, airport.latitude_deg, airport.longitude_deg, country.name,airport.continent "
            f"FROM country, airport "
            f"WHERE airport.iso_country = country.iso_country "
            f"having airport.ident = '{list_ident[0]}' OR ident= '{list_ident[1]}' OR ident= '{list_ident[2]}' OR ident= '{list_ident[3]}' OR ident= '{list_ident[4]}' OR ident= '{list_ident[5]}' OR ident= '{list_ident[6]}' OR ident= '{list_ident[7]}' OR ident= '{list_ident[8]}' OR ident= '{list_ident[9]}' OR ident='{list_ident[10]}' OR ident= '{list_ident[11]}'"
            f"order by airport.ident;")
        output = cursor.fetchall()
        for i in range(len(output)):
            airport_list[str(i+1)]=Airport(output[i][0],output[i][1], output[i][2], output[i][3], output[i][4], output[i][5], output[i][6])
        return airport_list
    except mysql.connector.errors.DatabaseError as e:
        return e