from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from bson.objectid import ObjectId
from flask_cors import CORS
import os
import requests

from Db import connect_to_db

app = Flask(__name__)
api = Api(app)
CORS(app)  

chat_collection = connect_to_db()
model_url = os.environ['MODEL_URI']

def new_chat(user_id):
    if user_id:
        chat = chat_collection.insert_one({
            'author': user_id,
            'title': 'New Chat',
            'conversation': [{
                'author': 'model',
                'message': 'Hi, Let"s start the convo!'
            }]
        })
        return chat.inserted_id


def insert_chat(user_type, author, chat_id, message):
    if user_type != 'model':
        chat = chat_collection.find_one({'_id': ObjectId(chat_id)})

        if len(chat['conversation']) == 1:
            chat['title'] = message
        
        if chat['author'] == author:
            chat['conversation'].append({
                'author': 'user',
                'message': message
            })

            chat_collection.update_one({'_id': ObjectId(chat_id)}, {"$set": chat})

            return {'result': 'inserted'}, 200
    else:
        chat = chat_collection.find_one({'_id': ObjectId(chat_id)})

        if chat['author'] == author:
            chat['conversation'].append({
                'author': 'ai',
                'message': message
            })

            chat_collection.update_one({'_id': ObjectId(chat_id)}, {"$set": chat})

            return {'result': 'inserted'}, 200


def getAns(query):
    try:
        res = requests.post(model_url + '/predict', json = {
            'query': query
        })

        return res.json()['response']

    except:
        return "The model is offline! please try again later!"



class Chats(Resource):
    def get(self):
        user_id = request.headers.get('user-id')

        if user_id:
            titles = []
            for chats in chat_collection.find({'author': user_id}):
                titles.append({ 
                    'title': chats['title'],
                    'id': str(chats['_id'])
                })
            return {'chats': titles}
        else:
            return {'chats': "No chats!"}


class ChatModel(Resource):
    def get(self, chat_id):
        user_id = request.headers.get('user-id')

        if chat_id == 'new':
            new_id = new_chat(user_id)

            return {'id': str(new_id)}
        
        if chat_id:
            chat = chat_collection.find_one({'_id': ObjectId(chat_id)})

            chat['_id'] = str(chat['_id'])
        return {'chat': chat}


class RAGModel(Resource):
    def post(self, chat_id):
        user_id = request.headers.get('user-id')
        req = request.json
        query = req['query']

        insert_chat('user', user_id, chat_id, query)

        response = getAns(query)

        insert_chat('model', user_id, chat_id, response)
        
        return {'response': response}

api.add_resource(RAGModel, '/query/<string:chat_id>')
api.add_resource(ChatModel, '/chat/<string:chat_id>')
api.add_resource(Chats, '/chats')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000)) 
    app.run(port=port, debug=True)