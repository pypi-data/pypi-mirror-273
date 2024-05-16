import flask
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_socketio import ConnectionRefusedError
from flask import request

from aipkgs_socketio import core


class SocketIOHelpers:
    class EventSubject:
        def __init__(self):
            self.observers = []

        def add_observer(self, observer):
            self.observers.append(observer)

        def remove_observer(self, observer):
            self.observers.remove(observer)

        def remove_all_observers(self):
            self.observers.clear()

        def notify_observers_on_connect(self, sid):
            for observer in self.observers:
                observer.on_connect(sid)

        def notify_observers_on_disconnect(self, sid):
            for observer in self.observers:
                observer.on_disconnect(sid)

    class EventObserver:
        def on_connect(self, sid):
            pass

        def on_disconnect(self, sid):
            pass

    event_subject = EventSubject()

    @staticmethod
    def setup():
        socketio = core.socketio()

        @socketio.on('connect')
        def connect(auth):
            sid = flask.request.sid
            print(f"New socket connected {sid}")
            print(f"request.headers.get('user'): {request.headers.get('user')}")

            SocketIOHelpers.event_subject.notify_observers_on_connect(sid)

            # print_with_filename(f'Client connected: {request.args.get("token")}')

            # if not self.authenticate(request.args):
            #     raise ConnectionRefusedError('unauthorized!')

        # broadcast=True
        # def ack():
        #     print_with_filename('message was received!')
        #
        # @socketio.on('my event')
        # def handle_my_custom_event(json):
        #     emit('my response', json, callback=ack)

        @socketio.on('disconnect')
        def disconnect():
            print('Client disconnected')
            sid = flask.request.sid
            SocketIOHelpers.event_subject.notify_observers_on_disconnect(sid)


        @socketio.on_error()  # Handles the default namespace
        def error_handler(e):
            print(f'error: {e}')

        @socketio.on_error_default  # handles all namespaces without an explicit error handler
        def default_error_handler(e):
            print(f'default error: {e}')

        # @socketio.on('message')
        # def handle_message(data):
        #     print_with_filename('received message: ' + data)
        #     send(data)
        #
        # @socketio.on('*')
        # def catch_all(event, sid, data):
        #     print_with_filename('catch all')
        #
        # @socketio.on('json')
        # def handle_json(json):
        #     print_with_filename('received json: ' + str(json))
        #     send({'key': 'bla bla bla'}, json=True)
        #
        # @socketio.on('my event')
        # def handle_my_custom_event(json):
        #     print_with_filename('received json: ' + str(json))
        #     emit('my response', json)
        #
        # def ack(arg):
        #     print_with_filename('message was received!')
        #     print_with_filename(f'arg: {arg}')
        #
        # @socketio.on('my_event')
        # def test_message(message):
        #     print_with_filename(f'test_message: {message}')
        #     print_with_filename(f'request.sid: {request.sid}')
        #     # print_with_filename(f"request.sid: {request.sid}")
        #     print_with_filename(f"request.headers.get('user'): {request.headers.get('user')}")
        #     print_with_filename(f"request.headers.get('user_payload'): {request.headers.get('user_payload')}")
        #     # emit('my_event', {'data': message}, room=sid, callback=ack)
        #     emit('my_event', {'data': message})
        #     # emit('my_event', {'data': message}, callback=ack)
        #     # emit('my response', {'data': message}, broadcast=True)
        #     # send('my response')
        #
        # @socketio.on('my_event', namespace='/call')
        # def test_message(message):
        #     print_with_filename(f'/call test_message: {message}')
        #     print_with_filename(f'request.sid: {request.sid}')
        #     emit('my_event', {'data': message})
        #
        # @socketio.event
        # def my_custom_event(arg1, arg2, arg3):
        #     print_with_filename('received args: ' + arg1 + arg2 + arg3)
        #
        # @socketio.on('my event', namespace='/test')
        # def handle_my_custom_namespace_event(json):
        #     print_with_filename('received json: ' + str(json))
        #
        # # def my_function_handler(data):
        # #     pass
        #
        # # socketio.on_event('my event', my_function_handler, namespace='/test')
        #
        # @socketio.on('my event')
        # def handle_my_custom_event(json):
        #     print_with_filename('received json: ' + str(json))
        #     return 'one', 2
        #
        # @socketio.on('my event', namespace='/test')
        # def handle_my_custom_namespace_event(json):
        #     print_with_filename('received message custom')
        #     # print_with_filename('received json: ' + str(json))
