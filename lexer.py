import token, sys, variable_dictionary

class Lexer():
	def __init__(self, block, dict):
		self.block = block
		self.dict = dict
		self.returns = []

	def error_out(self, err) :
		print('LEXER ERROR: ' + err)
		sys.exit(404)

	# Lexes / parses the block of tokenized code
	def lex(self):
		for i, line in enumerate(self.block):
			if line[0].token.is_instruction:

				# Handle verbal
				if line[0].token.show_name == 'VERBAL':
					line[0].token.function(self.dict, None, [], [line[0].data])
					continue

				returns = []
				if line[0].token.return_amount > 0:
					returns += line[1:][:line[0].token.return_amount]
				args = line[len(returns) + 1:]

				##### FOR DEBUG
				if line[0].token.show_name != 'INPUT':
					print ('\t', i, '\t->', line[0].token.show_name, end=' [ ')
					[print (str(x.data), end=', ') for x in returns]
					print ('] [', end=' ')
					for x in args:
						if x.token.show_name != 'BLOCK':
							print (str(x.data), end=', ')
						else:
							print ('{ ... }', end=', ')
					print (']')

				# Execute custom function
				if line[0].token.show_name == 'CUSTOM FUNCTION':

					# Create a new variable dictionary with arguments already assigned
					new_dict = variable_dictionary.VariableDictionary()
					new_dict.dictionary = dict(self.dict.dictionary)
					values = token.constants_of_list(new_dict, args)
					for i, value in enumerate(values):
						##### FOR DEBUG
						##### print (line[0].token.arguments[i].data, value)
						new_dict.dictionary[line[0].token.arguments[i].data] = value

					lexer = Lexer(line[0].token.function, new_dict)
					new_returns = lexer.lex()

					# Match return variable names
					for i, r in enumerate(returns):
						# if len(new_dict.lookup(new_returns[i].data)) != line[0].data:
						#	self.error_out('The value of ' + new_returns[i].data + ' did not match the specified bitcap for the instruction ' + line[0].token.id + '\nSpecified bitcap is ' + str(line[0].data) + ', but got ' + str(len(new_dict.lookup(new_returns[i].data))))
						self.dict.dictionary[r.data] = new_dict.lookup(new_returns[i].data)

					continue

				# If a return token is met, add the variables to the returns list
				if line[0].token.show_name == 'RETURN':
					self.returns += line[1:]

				# Execute current instruction
				if line[0].token.function is not None:
					line[0].token.function(self.dict, line[0].data, returns, args)


					##### FOR DEBUG
					##### print(self.dict.dictionary)
		return self.returns