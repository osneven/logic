import sys, re

class VariableDictionary():
	def __init__(self):
		self.dictionary = {}

	# Looks up af value from an variable identifier, errors out if identifier doesn't exist
	def lookup(self, identifier):

		# Check for index
		index = re.search('[0-9]+-', identifier[::-1])
		if index is not None:
			sub_str = index.group(0)
			identifier = identifier.replace(sub_str[::-1], '')
			index = int(sub_str.replace('-', ''))

		# Lookup variable
		try:
			value = self.dictionary[identifier]
			if index is not None:
				return value[index]
			return value
		except KeyError:
			print ('VARIABLE DICTIONARY ERROR: The variable identifier \'' + identifier + '\' has not yet been declared')
			sys.exit(404)
