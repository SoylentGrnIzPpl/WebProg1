from flask import render_template, request, redirect, url_for, make_response, session, flash
from app import app, db
from app.forms import LoginForm
from app.models import User

import datetime
import random
import json

from mongita import MongitaClientDisk
db_server = MongitaClientDisk(host="./.mongita")

@app.route('/')
def get_list():
    return render_template('gameList.html')


@app.route("/getMove")
def getMove():
    moveX = random.randrange(0, 7)
    data = { "data":[
        {
            "x": moveX
        }
    ]
    }
    return data

# @app.route("/findGame")
# def findGame():
#     game_db = db_server.game_db
#     game_list = game_db.game_list

#     for i in range(1,5):
#         game = game_list.find_one({"game":i,})
#         if game.p1 == 0 and game.p2 == 0:
            

@app.route("/connect4/<player>")
def connect4(player):
    game_db = db_server.game_db
    game_list = game_db.game_list
    game = game_list.find_one({'game':1})
    #print(game['p1'])
    # if game['p1'] == 0:
    #     player = 1
    #     createGame()
    # else:
    #     player = 2
    #     game_list.update_one({'game':1}, {'$set':{'p2':1}})
    # player = 1
    return render_template('connect4.html', player=player)

@app.route("/makeMove", methods=["POST"])
def makeMove():
    game_db = db_server.game_db
    game_list = game_db.game_list
    data = request.json
    query = 'col' + str(data['coordinate'][0]) + '.' + str(data['coordinate'][2])
    if data['player'] == 1:
        nextTurn = 2
    else:
        nextTurn = 1
    game_list.update_one({'game':1}, {'$set':{query:data['player']}})
    game_list.update_one({'game':1}, {'$set':{"time":datetime.datetime.now()}})
    game_list.update_one({'game':1}, {'$set':{"lastMove":str(data['coordinate'])}})
    game_list.update_one({'game':1}, {'$set':{"turn":nextTurn}})
    # coList = coordinate.split('-')
    # print(coList)
    
    print(data)

    return "data"

@app.route('/waitMove', methods=['GET'])
def waitMove():
    game_db = db_server.game_db
    game_list = game_db.game_list
    game = game_list.find_one({'game':1})
    turn = game['turn']
    lastMove = game['lastMove']
    restart = game['p1'] + game['p2']
    return json.dumps({"turn":turn, "lastMove":str(lastMove), "restart":restart})#str(turn) + '-' + str(lastMove)


@app.route('/createGame/<player>', methods=['GET'])
def createGame(player):
    game_db = db_server.game_db
    game_list = game_db.game_list
    game_list.update_one({'game':1}, {'$set':{str('p'+player):1}}) 
    game = game_list.find_one({'game':1})
    
    if game['p1'] == 1 and game['p2'] == 1 :
        game_list.delete_one({'game':1})
        game_list.insert_one({
            "game":1, 
            "p1":0,
            "p2":0,
            "turn":1,
            "time": datetime.datetime.now(),
            "lastMove": 9,
            "restart":0,

            "col0":[0,0,0,0,0,0],
            "col1":[0,0,0,0,0,0],
            "col2":[0,0,0,0,0,0],
            "col3":[0,0,0,0,0,0],
            "col4":[0,0,0,0,0,0],
            "col5":[0,0,0,0,0,0],
            "col6":[0,0,0,0,0,0],

        })
        return json.dumps({"restart":1})
    else:
        return json.dumps({"restart":0})