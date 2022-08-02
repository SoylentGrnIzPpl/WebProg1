from flask import render_template, request, redirect, url_for, make_response, session, flash
from app import app, db
from app.forms import LoginForm
from app.models import User

import datetime
import random
import json

from mongita import MongitaClientDisk
db_server = MongitaClientDisk(host="./.mongita")


"""
@app.route("/")
@app.route("/home")
def get_index():
    # username = request.cookies.get("username", None)
    if 'username' in session:
        username = session['username']
    else: 
        return redirect(url_for("get_login"))
    return render_template('home.html', name=username)

@app.route("/other")
def get_other():
    # username = request.cookies.get("username", None)
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for("get_login"))
    return render_template('other.html', name = username)

# @app.route("/hello")
# def get_hello():
#     return render_template('hello.html', name="Santa")

# @app.route("/hi")
# @app.route("/hi/<name>")
# def get_hi(name="Dick"):
#     name = name[::-1]
#     return render_template('hello.html', name=name)

@app.route("/login", methods=['GET'])
def get_login():
    # username = request.cookies.get("username", None)
    if 'username' in session:
        return redirect(url_for("get_index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('get_index'))
    return render_template('login.html', title='Login', form=form)

@app.route("/login", methods=['POST'])
def post_login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    # response = make_response(redirect(url_for('get_index')))
    # response.set_cookie("username", username)
    form = LoginForm()
    if form.validate_on_submit():#username != None and password != None:
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('get_login'))
        session['username'] = username
        return redirect(url_for('get_index'))
    else:
        flash('Username and Password fields must be filled.')
        return render_template('login.html', title='Login', form=form)
    # password = request.form.get("password", "<missing password>")
    # if password == "pass":
    #     return redirect(url_for('get_hi', name=username))
    # else:
    # return response

@app.route("/logout", methods=['GET'])
def get_logout():
    # response = make_response(redirect(url_for('get_login')))
    # response.delete_cookie("username")
    session.pop('username')
    return redirect(url_for('get_login'))
    # return response

@app.route("/register", methods=['GET'])
def get_register():
    if 'username' in session:
        return redirect(url_for("get_index"))
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def post_register():

    username = request.form.get("username", None)

    if(request.form.get("password", None) == request.form.get("repPassword", None)):
        password = request.form.get("password")
    else:
        flash('Passwords did not match.')
        return redirect(url_for('get_register'))

    if username != (None or '') and password != (None or ''):
        user = User.query.filter_by(username=username).first()
        if user is None:
            session['username'] = username
            user = User(username = username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration Successful!')
        else:
            flash('Username already taken.')
            return redirect(url_for('get_register'))
    else:
        flash('All fields must be filled.')
        return redirect(url_for('get_register'))
    return redirect(url_for('get_index'))
"""

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
    return str(turn) + '-' + str(lastMove)


@app.route('/createGame', methods=['GET'])
def createGame():
    game_db = db_server.game_db
    game_list = game_db.game_list
    
    game_list.delete_one({'game':1})
    game_list.insert_one({
    "game":1, 
    "p1":0,
    "p2":0,
    "turn":1,
    "time": datetime.datetime.now(),
    "lastMove": 9,

    "col0":[0,0,0,0,0,0],
    "col1":[0,0,0,0,0,0],
    "col2":[0,0,0,0,0,0],
    "col3":[0,0,0,0,0,0],
    "col4":[0,0,0,0,0,0],
    "col5":[0,0,0,0,0,0],
    "col6":[0,0,0,0,0,0],

    })

    return "success"