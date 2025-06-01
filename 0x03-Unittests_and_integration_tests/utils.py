import requests
from functools import wraps

def access_nested_map(nested_map, path):
	"""
	Access a nested dictionary following the keys in `path` (a tuple).
    Raise KeyError if any key is missing.
	"""
	current = nested_map
	for key in path:
		current = current[key]
	return current

def get_json(url):
	"""
	Send a GET request to the URL and return the JSON response.
	Raise requests.RequestException for any request errors.
	"""
	response = requests.get(url)
	response.raise_for_status()  # Raise an error for bad responses
	return response.json()

def memoize(func):
	"""
	Decorator to cache the return value of a function.
	"""
	cache = {}

	@wraps(func)
	def wrapper(*args, **kwargs):
		key = (args, tuple(sorted(kwargs.items())))
		if key not in cache:
			cache[key] = func(*args, **kwargs)
		# Return the cached value if it exists
		return cache[args]

	return wrapper