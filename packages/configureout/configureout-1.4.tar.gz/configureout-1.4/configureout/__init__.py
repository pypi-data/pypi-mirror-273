import json


class Config(object):
	def __init__(self, config_file=None, /, config=None, encoding='utf-8'):
		if config_file:
			with open(config_file, 'r', encoding=encoding) as config_file:
				config = json.loads(config_file.read())

		if type(config) != dict:
			raise TypeError(f'Config must be a dict, not {type(config)}')

		self.__keys = list(config.keys())
		self.__index = 0

		for k, v in config.items():
			if isinstance(v, (list, tuple)):
				setattr(self, k, [Config(config=x) if isinstance(x, dict) else x for x in v])
			else:
				setattr(self, k, Config(config=v) if isinstance(v, dict) else v)

	def __getitem__(self, key):
		return getattr(self, key)

	def __len__(self):
		return len(self.__keys)
		
	def __iter__(self):
		return self
	
	def __next__(self):
		if self.__index >= len(self.__keys):
			self.__index = 0
			raise StopIteration

		key = self.__keys[self.__index]
		self.__index += 1
		return key, getattr(self, key)

	def get(self, key, default=None):
		return getattr(self, key, default)

	def keys(self):
		return (k for k in self.__keys)

	def values(self):
		return (getattr(self, k) for k in self.__keys)
	
	def items(self):
		return ((k, getattr(self, k)) for k in self.__keys)