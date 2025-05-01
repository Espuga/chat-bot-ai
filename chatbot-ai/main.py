from mongodb import MongoDBConnection
from flask import Flask, jsonify, request
from flask_cors import CORS
import ollama
from werkzeug.utils import secure_filename

connection = MongoDBConnection()

def process_messages(chat_id):
  info_list = connection.get_info()
  messages_list = connection.get_messages(chat_id)

  information = "\n\n".join([info["text"] for info in info_list])
  # messages = [{'role': msg['role'], 'content': msg['message']} for msg in messages_list]
  
  prompt = f"""
  Given the following text, answer the questions:

  Text:
  \"\"\"{information}\"\"\"
  """
  messages = [{'role': 'system', 'content': prompt}] + [{'role': msg['role'], 'content': msg['message']} for msg in messages_list]


  response = ollama.chat(model='mistral', messages=messages)
  messages.append({'role': 'assistant', 'content': response['message']['content']})

  connection.add_message(chat_id, "assistant", response['message']['content'])

  assistant_response = {
    'role': 'assistant',
    'message': response['message']['content']  # Make sure this is the right field to extract
  }
  return assistant_response


def serialize(object):
  object["_id"] = str(object["_id"])  # Convert ObjectId to string
  return object
def serialize_message(object):
  object["_id"] = str(object["_id"])  # Convert ObjectId to string
  object["chat_id"] = str(object["chat_id"])  # Convert ObjectId to string
  return object

app = Flask(__name__)
CORS(app)

# Get all chats
@app.route('/chats', methods=['GET'])
def get_chats():
  chats = connection.get_chats()
  return jsonify([serialize(chat) for chat in chats])

@app.route('/chats', methods=['POST'])
def add_chat():
  data = request.get_json()
  chat_id = connection.add_chat(data["name"])
  return jsonify(serialize(chat_id)), 201

@app.route('/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
  connection.delete_chat(chat_id)
  return jsonify({"message": "Chat deleted successfully"}), 200

# Get messages for a specific chat
@app.route('/chats/<chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
  messages = connection.get_messages(chat_id)
  return jsonify({ "loading": connection.get_chat_loading(chat_id), "messages": [serialize_message(message) for message in messages] })

# New message for a specific chat
@app.route('/chats/<chat_id>/messages', methods=['POST'])
def add_message(chat_id):
  data = request.get_json()
  # Add loading message
  connection.update_chat_loading(chat_id, True)
  connection.add_message(chat_id, "user", data["message"])
  answer = process_messages(chat_id)
  connection.update_chat_loading(chat_id, False)

  return jsonify(answer), 201


@app.route('/info', methods=['GET'])
def get_info():
  info = connection.get_info()
  return jsonify([serialize(info) for info in info])

@app.route('/info/<info_id>', methods=['DELETE'])
def delete_info(info_id):
  connection.delete_info(info_id)
  return jsonify({"message": "Info deleted successfully"}), 200

@app.route('/info', methods=['POST'])
def add_info():
  file = request.files['file']
  filename = secure_filename(file.filename)
  file_text = file.read().decode('utf-8', errors='ignore')
  added_file = connection.add_info(filename, file_text)
  return jsonify(serialize(added_file)), 201


if __name__ == '__main__':
  app.run(debug=False)