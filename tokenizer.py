import token, re, sys

def tokenize(raw_code):
	tokenizer = Tokenizer(raw_code)
	block = []
	current_line = []
	for i, tokendata in enumerate(tokenizer):
		if not tokendata:
			break
		elif tokendata == 'TERMINATE':
			block.append(current_line)
			current_line = []
			continue
		else:
			current_line.append(tokendata)
		if tokendata.token.show_name == 'VERBAL':
			block.append(current_line)
			current_line = []

		##### FOR DEBUG
		if tokendata.token.show_name != 'BLOCK':
			print('\t', i, '\t->', tokendata.token.show_name, '=', str(tokendata.data))

		#if len(current_line) != 0:
		#	block.append(current_line)
	return block

class Tokenizer():
	def __init__(self, raw_code):
		self.raw_code = re.sub('\s+', ' ', raw_code) + 'EOF'
		##### FOR DEBUG
		##### print (self.raw_code)
		self.instruction = None
		self.argument_index = 0
		self.terminated = False
		self.default_bitcap = None
		self.next_bitcap = None
		self.function_line = []

	def __iter__(self):
		return self

	def __next__(self):
		tokendata, i = self.next_token() # Get the next token in the raw code
		if not tokendata:
			return False
		elif tokendata == 'TERMINATE':
			return 'TERMINATE'
		self.raw_code = self.raw_code[i+1:] # Remove said token from the raw code
		return tokendata

	# Errors out and exits
	def error_out(self, err) :
		print('TOKENIZER ERROR: ' + err)
		sys.exit(404)

	# Token data to return
	def return_token_data(self, tokendata, i):
		if self.instruction.show_name == 'FUNCTION':
			self.function_line.append(tokendata)
		return [tokendata, i]

	# Finds and returns the next token in the raw code
	def next_token(self):

		# If instruction was terminated
		if self.terminated:
			# Not enough arguments or return variables
			if self.instruction.argument_amount + self.instruction.return_amount != self.argument_index and self.instruction.finite_arguments:
				tmp = self.instruction.show_name
				if tmp == 'CUSTOM FUNCTION' :
					tmp = self.instruction.id
				self.error_out('Expected ' + str(self.instruction.argument_amount) + ' arguments and ' + str(self.instruction.return_amount) + ' return variables for the instruction ' + tmp + ', (' + str(self.instruction.argument_amount + self.instruction.return_amount) + ') in total, but found ' + str(self.argument_index) + ' tokens overall')

			self.terminated = False
			self.instruction = None
			self.function_line = []
			return ['TERMINATE', 0]

		raw_chunk = ''
		for i,character in enumerate(self.raw_code):

			# Handle terminator
			if character == ';':
				if len(raw_chunk.strip()) - 1 < 0 or (raw_chunk.strip()[0] != '{' or raw_chunk.strip()[len(raw_chunk.strip()) - 1] == '}'):
					self.terminated = True
					character = ' '

			# Append character to the raw chunk, remove leading spaces
			raw_chunk += character
			while len(raw_chunk) > 0 and raw_chunk[0] == ' ':
				raw_chunk = raw_chunk[1:]

			##### FOR DEBUG
			##### print (raw_chunk)

			# Find matching token
			for t in token.tokens:
				if (not t.is_regex and t.id == raw_chunk) or (t.is_regex and re.match(t.id, raw_chunk)): # Match found

					# Handle both verbal and non-verbal comments
					if t.show_name == 'COMMENT':
						raw_chunk = ''
						break
					if t.show_name == 'VERBAL':
						return [token.TokenData(t, raw_chunk.replace('"', '')), i]

					# Instruction undergoing ...
					if self.instruction is not None:
						# Error if new instruction appears
						if t.is_instruction:
							self.error_out('The instruction ' + t.show_name + ' not expected at this time\nThe instruction ' + t.show_name + ' needs ' + str(self.instruction.argument_amount) + ' arguments but found ' + str(self.argument_index))
						else:

							# Allow more tokens for the instruction
							if self.instruction.argument_amount + self.instruction.return_amount != self.argument_index or not self.instruction.finite_arguments:

								# If more return variables are needed, check that the token is a variable
								if self.instruction.return_amount > self.argument_index and t.show_name != 'VARIABLE':
									tmp = self.instruction.show_name
									if tmp == 'CUSTOM FUNCTION' :
										tmp = self.instruction.id
									self.error_out('Expected ' + str(self.instruction.return_amount) + ' return variables for the instruction ' + tmp + ', but found ' + str(self.argument_index))

								self.argument_index += 1

								# If it's a block, tokenize it
								if t.show_name == 'BLOCK':
									print ('\n\t<-- START BLOCK')
									block = tokenize(raw_chunk.strip()[1 :len(raw_chunk) - 2])
									print('\tSTART BLOCK -->\n')

									for line in block:
										for tokendata in line:
											print (tokendata.token.show_name)

								# If block belongs to a function, declare the function with the block
									if self.instruction.show_name == 'FUNCTION':

										# Find return amount
										return_amount = 0
										for line in block:
											if line[0].token.show_name == 'RETURN':
												return_amount = len(line) - 1

										# Append the function to the token list
										custom_func = token.Token('CUSTOM FUNCTION', self.function_line[0].data, False, True, len(self.function_line) - 1, True, return_amount, block)
										custom_func.arguments = self.function_line[1:]
										token.tokens.append(custom_func)
										##### FOR DEBUG
										##### [ print ('*', x.data) for x in self.function_line ]
										##### [ print ('---', x.show_name, ':', x.id) for x in token.tokens ]

									return self.return_token_data(token.TokenData(t, block), i)

								return self.return_token_data(token.TokenData(t, raw_chunk.replace('$', '').strip()), i)

							# Disallow ...
							elif self.instruction.argument_amount + self.instruction.return_amount > 0:
								tmp = self.instruction.show_name
								if tmp == 'CUSTOM FUNCTION':
									tmp = self.instruction.id
								self.error_out('Expected ' + str(self.instruction.argument_amount) + ' arguments and ' + str(self.instruction.return_amount) + ' return variables for the instruction ' + tmp + ', (' + str(self.instruction.argument_amount + self.instruction.return_amount) + ') in total, but found ' + str(self.argument_index) + ' tokens overall')

					# No previous instruction
					else:

						# Handle new instruction
						if t.is_instruction:
							if self.next_bitcap is None and t.show_name != 'FUNCTION' and t.show_name != 'EXIT':
								self.error_out('No bitcap specified for the instruction ' + t.show_name)

							self.instruction = t
							self.argument_index = 0
							r = [token.TokenData(t, self.next_bitcap), i]
							if self.next_bitcap != self.default_bitcap:
								self.next_bitcap = self.default_bitcap
							return r

						# Handle bitcap and default bitcap
						elif t.show_name.replace('DEFAULT ', '') == 'BITCAP':
							bitcap = raw_chunk.replace('@', '').strip()
							if bitcap.isdigit():
								if t.show_name[:7] == 'DEFAULT':
									self.default_bitcap = int(bitcap)
									self.next_bitcap = self.default_bitcap
								else:
									self.next_bitcap = int(bitcap)
								raw_chunk = ''
							else:
								self.error_out('The bitcap must be an integer')
						else:
							self.error_out('Expected an instruction but found type ' + t.show_name)

		# Return none on end of file
		if len (raw_chunk) >= 3 and raw_chunk[:3] == 'EOF':
			if self.instruction is not None and self.instruction.argument_amount + self.instruction.return_amount != self.argument_index and self.instruction.finite_arguments :
				tmp = self.instruction.show_name
				if tmp == 'CUSTOM FUNCTION' :
					tmp = self.instruction.id
				self.error_out('Expected ' + str(self.instruction.argument_amount) + ' arguments and ' + str(self.instruction.return_amount) + ' return variables for the instruction ' + tmp + ', (' + str(self.instruction.argument_amount + self.instruction.return_amount) + ') in total, but found ' + str(self.argument_index) + ' tokens overall')

			else:
				return [None, None]
		else:
			self.error_out('Missing EOF or unknown token on last line')