import sys, re

class Token:
	def __init__(self, show_name, id, is_regex, is_instruction, argument_amount, finite_arguments, return_amount, function):
		self.show_name = show_name
		self.id = id
		self.is_regex = is_regex
		self.is_instruction = is_instruction
		self.finite_arguments = finite_arguments
		self.argument_amount = argument_amount # Use -1 for infinite
		self.arguments = [] # For custom functions
		self.return_amount = return_amount
		self.function = function

class TokenData:
	def __init__(self, token, data):
		self.token = token
		self.data = data

# Bitcap overflow exception
def bitcap_err():
	print ('LEXER ERROR: A bit length did not match the specified bitcap')
	sys.exit(404)

# Convert all instances of type VARIABLE in a list to it's value
def constants_of_list(dict, list):
	values = []
	for i,item in enumerate(list):
		if item.token.show_name == 'VARIABLE':
			values.append(dict.lookup(item.data))
		else:
			values.append(item.data)
	return values

########## Init build-in instruction functions

# Assigns a value to a variable
def ins_assignment(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	value = ''
	for arg in args:
		value += arg

	if len(value) != bitcap:
		bitcap_err()
	else:
		dict.dictionary[returns[0].data] = value

# Assigns the user input to a variable
def ins_input(dict, bitcap, returns, args):
	value = input()
	if re.match('[01]+', value):
		if len(value) != bitcap:
			bitcap_err()
		else:
			dict.dictionary[returns[0].data] = value
	else:
		print ('LEXER ERROR: The given input needs to be a binary integer')
		sys.exit(404)

# The bitwise NOT operator
def ins_not(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	value = args[0]
	not_value = ''
	for c in value:
		if c == '0':
			not_value += '1'
		elif c == '1':
			not_value += '0'
	if len(not_value) != bitcap:
		bitcap_err()
	else:
		dict.dictionary[returns[0].data] = not_value

# The bitwise AND operator
def ins_and(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	and_value = ''
	prev = None
	for arg in args:
		and_value = ''
		if prev is None:
			prev = arg
			continue
		else:
			for i,c in enumerate(prev):
				if c == '1' and arg[i] == '1':
					and_value += '1'
				else:
					and_value += '0'
			prev = and_value
	if len(and_value) != bitcap :
		bitcap_err()
	else :
		dict.dictionary[returns[0].data] = and_value

# THe bitwise OR operator
def ins_or(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	or_value = ''
	prev = None
	for arg in args :
		or_value = ''
		if prev is None :
			prev = arg
			continue
		else :
			for i, c in enumerate(prev) :
				if c == '1' or arg[i] == '1' :
					or_value += '1'
				else :
					or_value += '0'
			prev = or_value
	if len(or_value) != bitcap :
		bitcap_err()
	else :
		dict.dictionary[returns[0].data] = or_value

# The bitwise NAND operator
def ins_nand(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	and_value = ''
	prev = None
	for arg in args :
		and_value = ''
		if prev is None :
			prev = arg
			continue
		else :
			for i, c in enumerate(prev) :
				if c == '1' and arg[i] == '1' :
					and_value += '0'
				else :
					and_value += '1'
			prev = and_value
	if len(and_value) != bitcap :
		bitcap_err()
	else :
		dict.dictionary[returns[0].data] = and_value

# The bitwise NOR operator
def ins_nor(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	or_value = ''
	prev = None
	for arg in args :
		or_value = ''
		if prev is None :
			prev = arg
			continue
		else :
			for i, c in enumerate(prev) :
				if c == '1' or arg[i] == '1' :
					or_value += '0'
				else :
					or_value += '1'
			prev = or_value
	if len(or_value) != bitcap :
		bitcap_err()
	else :
		dict.dictionary[returns[0].data] = or_value

# The bitwise XOR operator
def ins_xor(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	and_value = ''
	prev = None
	for arg in args :
		and_value = ''
		if prev is None :
			prev = arg
			continue
		else :
			for i, c in enumerate(prev) :
				if c != arg[i]:
					and_value += '1'
				else :
					and_value += '0'
			prev = and_value
	if len(and_value) != bitcap :
		bitcap_err()
	else :
		dict.dictionary[returns[0].data] = and_value

# The bitwise XNOR operator
def ins_xnor(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	and_value = ''
	prev = None
	for arg in args :
		and_value = ''
		if prev is None :
			prev = arg
			continue
		else :
			for i, c in enumerate(prev) :
				if c == arg[i] :
					and_value += '1'
				else :
					and_value += '0'
			prev = and_value
	if len(and_value) != bitcap :
		bitcap_err()
	else :
		dict.dictionary[returns[0].data] = and_value

# Prints a message to the screen
def ins_verbal(dict, bitcap, returns, args):
	value = args[0]
	if len(value) < 1:
		return

	# Replace variable identifiers with that variable's value
	human = value[0] == '^'
	if human:
		value = value[1:]
	for var in dict.dictionary:
		lookup = dict.lookup(var)
		if human:
			lookup = str(int(lookup, 2))
		value = value.replace('$' + var, lookup)

	chunk = ''
	for c in value:
		chunk += c

		# Handle special character escapes
		if len(chunk) > 2:
			two = chunk[-2:]
			if two == '\\n':
				print ()
				continue
			elif two == '\\t':
				print('\t', end='')
				continue
			elif two == '\\\\':
				print('\\', end='')
				continue
			elif two == '\\|':
				print ('|', end='')
				continue

		if c != '\\' and c != '|':
			print (c, end='')

	if value[-1:] != '|':
		print ()

# Exits the program
def ins_exit(dict, bitcap, returns, args):
	args = constants_of_list(dict, args)
	print ('Terminating with exit code', args[0], '...')
	sys.exit()

########## Init tokens
tokens = []

# Instructions
tokens.append(Token('ASSIGNMENT', 	'LET', 	False, True, 1, False, 1, ins_assignment))
tokens.append(Token('INPUT', 		'READ', False, True, 0, True,  1, ins_input))
tokens.append(Token('VERBAL', 		'".*"', True,  True, 0, True,  0, ins_verbal))
tokens.append(Token('FUNCTION', 	'func', False, True, 0, False, 0, None))
tokens.append(Token('RETURN',		'RETURN', False, True, 1, False, 0, None))
tokens.append(Token('EXIT',			'EXIT', False, True, 1, True, 0, ins_exit))

# Bitwise instructions
tokens.append(Token('NOT',  'NOT', 	False, True, 1, True,  1, ins_not))
tokens.append(Token('AND',  'AND', 	False, True, 2, False, 1, ins_and))
tokens.append(Token('OR',   'OR', 	False, True, 2, False, 1, ins_or))
tokens.append(Token('NAND', 'NAND', False, True, 2, False, 1, ins_nand))
tokens.append(Token('NOR',  'NOR', 	False, True, 2, False, 1, ins_nor))
tokens.append(Token('XOR',  'XOR', 	False, True, 2, False, 1, ins_xor))
tokens.append(Token('XNOR', 'XNOR', False, True, 2, False, 1, ins_xnor))

# Values
tokens.append(Token('CONSTANT', '[01]+ ', 				True, False, None, None, None, None))
tokens.append(Token('VARIABLE', '\$[0-9a-zA-Z_-]+ ', 	True, False, None, None, None, None))
tokens.append(Token('BLOCK', 	'{.*} ', 				True, False, None, None, None, None))

# Bitcap
tokens.append(Token('BITCAP', 			'[1-9][0-9]*@',	True, False, None, None, None, None))
tokens.append(Token('DEFAULT BITCAP', 	'@[1-9][0-9]*', True, False, None, None, None, None))

# Comment
tokens.append(Token('COMMENT', '\'.*\'', True, False, None, None, None, None))
