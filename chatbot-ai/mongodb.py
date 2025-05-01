from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

class MongoDBConnection:
  def __init__(self):
    self.client = MongoClient("mongodb://admin:admin@localhost:27017/")
    self.db = self.client["chat"]

  def get_chats(self):
    chats = self.db["chats"]
    return list(chats.find())
  
  def add_chat(self, chat_name: str):
    chats = self.db["chats"]
    result = chats.insert_one({"name": chat_name, "timestamp": datetime.now()})
    new_chat = chats.find_one({"_id": result.inserted_id})
    return new_chat
  
  def delete_chat(self, chat_id):
    # Convert chat_id string to ObjectId
    if isinstance(chat_id, str):
      try:
        chat_id = ObjectId(chat_id)
      except:
        print("Invalid ObjectId format")
        return False

    messages = self.db["messages"]
    messages.delete_many({"chat_id": chat_id})
    chats = self.db["chats"]
    result = chats.delete_one({"_id": chat_id})
    return result.deleted_count > 0
  
  def get_messages(self, chat_id):
    # Convert chat_id string to ObjectId
    if isinstance(chat_id, str):
      try:
        chat_id = ObjectId(chat_id)
      except:
        print("Invalid ObjectId format")
        return []

    messages = self.db["messages"]
    return list(messages.find({"chat_id": chat_id}))
  
  def add_message(self, chat_id, role: str, message: str):
    # Convert chat_id string to ObjectId
    if isinstance(chat_id, str):
      try:
        chat_id = ObjectId(chat_id)
      except:
        print("Invalid ObjectId format")
        return False

    messages = self.db["messages"]
    result = messages.insert_one({"chat_id": chat_id, "message": message, "role": role, "timestamp": datetime.now()})
    return result.inserted_id
  
  def get_info(self):
    info = self.db["info"]
    return list(info.find())
  
  def delete_info(self, info_id):
    info = self.db["info"]
    result = info.delete_many({ "_id": ObjectId(info_id)})
    return result.deleted_count > 0
  
  def add_info(self, file_name: str, info_text: str):
    info = self.db["info"]
    result = info.insert_one({"text": info_text, "file_name": file_name, "timestamp": datetime.now()})
    new_info = info.find_one({"_id": result.inserted_id})
    return new_info

  def update_chat_loading(self, chat_id, loading: bool):
    # Convert chat_id string to ObjectId
    if isinstance(chat_id, str):
      try:
        chat_id = ObjectId(chat_id)
      except:
        print("Invalid ObjectId format")
        return False

    chats = self.db["chats"]
    result = chats.update_one({"_id": chat_id}, {"$set": {"loading": loading}})
    return result.modified_count > 0
  
  def get_chat_loading(self, chat_id):
    # Convert chat_id string to ObjectId
    if isinstance(chat_id, str):
      try:
        chat_id = ObjectId(chat_id)
      except:
        print("Invalid ObjectId format")
        return False

    chats = self.db["chats"]
    chat = chats.find_one({"_id": chat_id})
    return chat.get("loading", False) if chat else False