from . import BASE, SESSION, users_collection
from config import vars
ID = vars.OWNER_ID

class Users:
    def adduser(user_id):
        if users_collection.find_one({"user_id": user_id}) is None:
            users_collection.insert_one({"user_id": user_id})
  
    def count():
         return users_collection.count_documents({})
    
    def get_all_users():
        return list(users_collection.find())
        
    def promote(userid):
        users_collection.update_one({'user': int(userid)}, {"$set": {'is_sudo': True}})
        return True
        
    def demote(userid):
        users_collection.update_one({'user': int(userid)}, {"$set": {'is_sudo': False}})
        return True

    def is_sudo(userid):
        x = users_collection.find_one({'user': int(userid)})
        if x is not None:
            return x['is_sudo']
        else:
            return False
     
    def is_reg(userid):
        x = users_collection.find_one({'user': int(userid)})
        if x is None:
            return False
        else:
            return True


if Users.is_reg(int(ID)) is False:
    Users.adduser(ID)
    Users.promote(ID)                       
