import json

from flask import session
from flask_socketio import join_room, leave_room
from ..extensions import redis_store, socketio
from ..tasks import send_message
from ..utils import is_json


@socketio.on('connect')
def connect():
    session['users'] = []


@socketio.on('disconnect')
def disconnect():
    for user in session['users']:
        leave_room(user)
        session['users'].remove(user)
        redis_store.srem("messenger:users", user)


@socketio.on('register')
def register(data):
    if 'user' in data and data['user'] != "":
        join_room(data['user'])
        session['users'].append(data['user'])
        redis_store.sadd("messenger:users", data['user'])
        return True
    else:
        return False


@socketio.on('unregister')
def unregister(data):
    if 'user' in data and data['user'] != "":
        leave_room(data['user'])
        session['users'].remove(data['user'])
        redis_store.srem("messenger:users", data['user'])
        return True
    else:
        return False


@socketio.on('send')
def send(data):
    if 'user' in data and data['user'] != "" and 'message' in data:
        if redis_store.sismember("messenger:users", data['user']):
            if 'event' in data and data['event'] != "":
                send_message.delay(data['message'],
                                   data['user'],
                                   data['event'])
            else:
                send_message.delay(data['message'], data['user'])
            return True
    return False


@socketio.on('send_json')
def send_json(data):
    if ('user' in data and data['user'] != "" and
            'message' in data and is_json(data['message'])):
        if redis_store.sismember("messenger:users", data['user']):
            json_object = json.loads(data['message'])
            if 'event' in data and data['event'] != "":
                send_message.delay(json_object, data['user'], data['event'])
            else:
                send_message.delay(json_object, data['user'])
            return True
    return False
