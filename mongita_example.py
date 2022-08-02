from mongita import MongitaClientDisk
from bson.objectid import ObjectId

client = MongitaClientDisk(host="./.mongita")

shopping_db = client.shopping_db
shopping_list = shopping_db.shopping_list
shopping_list.delete_many({})

shopping_list.insert_one({"description":"apple"})
shopping_list.insert_one({"description":"milk"})
shopping_list.insert_one({"description":"cheese"})

print(list(shopping_list.find({})))

items = list(shopping_list.find({}))
items = [item['description'] for item in items]
print(items)

shopping_list.insert_one({"description":"banana"})

items = list(shopping_list.find({}))
items = [item['description'] for item in items]
print(items)

shopping_list.delete_one({"description":"banana"})

items = list(shopping_list.find({}))
items = [item['description'] for item in items]
print(items)

shopping_list.update_one({"description":"apple"}, {'$set':{"description":"pear"}})
#shopping_list.update_one({"description":{"$gt":"lava"}}, {"$set":{"description":"cookie"}})

items = list(shopping_list.find({}))
items = [item['description'] for item in items]
print(items)

pear_item = shopping_list.find_one({"description":"pear"})
#pear_item = [pear_item['description']]
print(pear_item)

#pear_id = pear_item['_id']
pear_id = str(pear_item['_id'])
pear_id = ObjectId(pear_id)
print([pear_id])
# pear_id = str(pear_id)
# print([pear_id])
#_id = ObjectID(pear_id)

#shopping_list.update_one({"_id":pear_id}, {'$set':{"description":"rapple"}})
shopping_list.delete_one({'_id':pear_id})

items = list(shopping_list.find({}))
items = [item['description'] for item in items]
print(items)