from .extensions import celery, socketio


@celery.task()
def send_message(message, user, event=None):
	if event is None:
		event = 'message'
	socketio.emit(event, message , room=user)