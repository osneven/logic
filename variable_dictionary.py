import sys, re

class VariableDictionary():
	def __init__(self):
		self.dictionary = {}

	# Looks up af value from an variable identifier, errors out if identifier doesn't exist
	def lookup(self, identifier):

		# Check for index
		index = re.search('-[0-9]+', identifier)
		if index is not None:
			ss = index.group(0)
			identifier = identifier.replace(ss, '')
			ss = ss.replace('-', '')
			index = int(ss)


		# Lookup variable
		try:
			value = self.dictionary[identifier]
			if index is not None:
				if index < len(str(value)):
					return value[index]
				else:
					print ('VARIABLE ERROR: The value of', value, 'does not have an index of', index)
					sys.exit(404)
			return value
		except KeyError:
			print ('VARIABLE DICTIONARY ERROR: The variable identifier \'' + identifier + '\' has not yet been declared')
			sys.exit(404)
