from mongita import MongitaClientDisk
import datetime
client = MongitaClientDisk(host="./.mongita")

shopping_db = client.shopping_db
shopping_list = shopping_db.shopping_list
shopping_list.delete_many({})

game_db = client.game_db
game_list = game_db.game_list
game_list.delete_many({})

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

game = game_list.find_one({'game':1})
print(game['time'])
if game['p1'] == 0:
    print(game['p1'])

# game_list.update_one({'game':1}, {'$set':{'turn':3}})
# game_list.update_one({'game':1}, {'$set':{'col0.0':3}})
# game_list.update_one({'game':1}, {'$set':{'col0.3':99}})


items = game_list.find({"game":1})
items = list(items)
print(items)


#shopping_list.insert_one({})
shopping_list.insert_one({"desc":"milk"})
shopping_list.insert_one({"desc":"apple"})
shopping_list.insert_one({"desc":"cheese"})
shopping_list.insert_one({"desc":"cookies"})
shopping_list.insert_one({"desc":"hot dogs"})
shopping_list.insert_one({"desc":"mustard"})

# items = list(shopping_list.find({}))
# items = [item['desc'] for item in items]
# print(items)