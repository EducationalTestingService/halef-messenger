import json


def is_string_or_unicode(s):
	"""
	Determine whether or not this object is a string or unicode.

	:param s: object
	:return: bool
	"""
	return isinstance(s, basestring)


def is_json(s):
	"""
	Determine whether or not this object can be converted into JSON.
	
	
	:param s: object
	:return: bool
	"""
	if is_string_or_unicode(s):
		try:
			json_object = json.loads(s)
			return True
		except:
			pass
	return False