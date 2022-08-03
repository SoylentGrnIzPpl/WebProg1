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
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list

    the_list = list(shopping_list.find({}))

    print(the_list)

    return render_template('list.html', list=the_list)

@app.route("/data")
def get_data():
    data = { "data":[
        {
            "_id": "alkdfja;s",
           "desc": "apples"
        },
        {
            "_id": ";asldkfjas;lj",
            "desc": "oranges"
        }
    ]
    }
    return data

@app.route('/add_item', methods=['GET'])
def get_add_item():
    return render_template('add_item.html')

@app.route('/add_item', methods=['POST'])
def post_add_item():
    desc = request.form.get("desc", "<missing description>")
    print("adding ",desc)
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    shopping_list.insert_one({'desc':desc})

    return redirect(url_for('get_list'))

@app.route("/delete_item/<id>", methods=['GET'])
def get_delete_item(id):
    print("deleting id=",id)
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    shopping_list.delete_one({'_id':id})

    return redirect(url_for('get_list'))

@app.route("/update_item/<id>", methods=['GET'])
def get_update_item(id):
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    the_item = shopping_list.find_one({"_id":id})
    return render_template('update_item.html',item=the_item)

from bson.objectid import ObjectId

@app.route("/update_item", methods=['POST'])
def post_update_item():
    _id = request.form.get("_id", "<missing _id>")
    desc = request.form.get("desc", "<missing desc")
    print("updating id=",_id)
    print("updating desc=",desc)
    shopping_db = db_server.shopping_db
    shopping_list = shopping_db.shopping_list
    _id = ObjectId(_id)
    shopping_list.update_one({'_id':_id}, {"$set" : {"desc": desc}})
    return redirect(url_for('get_list'))

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