import json

from flask import jsonify, request, current_app

from . import api
from .exceptions import APIError
from ..tasks import send_message
from ..extensions import redis_store
from ..utils import is_json


@api.errorhandler(APIError)
def handle_api_error(error):
	"""Handles APIError exceptions gracefully."""
	response = jsonify(error.to_dict())
	return (response, error.status_code)


@api.route("/send", methods=['POST'])
def send():
	"""Endpoint to forward messages."""
	if current_app.debug:
		current_app.logger.debug("Received request {}".format(request))
		current_app.logger.debug(request.headers)
		current_app.logger.debug(request.form)

	args = validate_send_request(request)

	if redis_store.sismember("messenger:users", args['user']):
		if 'event' in args and args['event'] != "":
			send_message.delay(args['message'], args['user'], args['event'] )
		else:
			send_message.delay(args['message'], args['user'])
		return jsonify(True)
	return jsonify(False)


@api.route("/send_json", methods=['POST'])
def send_json():
	"""Endpoint to forward JSON messages."""
	args = validate_send_request(request)

	if redis_store.sismember("messenger:users", args['user']):
		if is_json(args['message']):
			json_object = json.loads(args['message'])
			if 'event' in args and args['event'] != "":
				send_message.delay(json_object, args['user'], args['event'] )
			else:
				send_message.delay(json_object, args['user'])
			return jsonify(True)
		else:
			err_msg = '"message" is not valid JSON'
			raise APIError(err_msg);
	return jsonify(False)


def validate_send_request(request):
	"""Determines if the request to send or send_json is valid.

	:param request: The request
	:return: parsed arguments
	"""
	if not (request.headers['Content-Type'] ==
			'application/x-www-form-urlencoded'):
		err_msg = 'Content-Type must be application/x-www-form-urlencoded'
		raise APIError(err_msg, status_code=415)

	# Check if all required parameters are available and non-empty
	form_data = request.form
	required_params = ('user', 'message')
	if (form_data is None
			or not all(param in form_data for param in required_params)
			or any(form_data[param] == "" for param in required_params)):
		err_msg = 'Required parameters are {}'.format(', '.join(required_params))
		raise APIError(err_msg)

	return form_data

