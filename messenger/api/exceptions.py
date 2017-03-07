class APIError(Exception):
	"""Custom APIError handled in http.py.
	
	:param status_code: HTTP status code to use in response
	:param payload: Additional payload to send with response
	:param reason: Explanation why the error occured

	"""
	status_code = 400

	def __init__(self, err_msg, status_code=None, additional_payload=None):
		Exception.__init__(self)
		self.err_msg = err_msg
		if status_code is not None:
			self.status_code = status_code
		self.payload = additional_payload


	def to_dict(self):
		"""Converts the APIError instance into dict for response.

		:return: dict
		"""
		rv = dict(self.payload or ())
		rv['error'] = self.err_msg
		return rv