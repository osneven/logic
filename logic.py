'''

	The LOGIC interpreter
	Author: Oliver S. Neven
	Written in 2016

	This python program is used to execute LOGIC programs  and .logic files
	For executing a .logic file run:
		python ./logic.py path/to/file.logic

'''

import sys, tokenizer, lexer, os, variable_dictionary

sys.argv.append('sample/sample0.logic')

if len(sys.argv) >= 1:
	if os.path.exists(sys.argv[1]):
		file = open(sys.argv[1], 'r')
		raw_code = file.read()

		##### FOR DEBUG
		print ('\n---------- Tokenizing ----------\n')

		block = tokenizer.tokenize(raw_code)

		##### FOR DEBUG
		print ('\n----------  Parsing  -----------\n')

		lexer = lexer.Lexer(block, variable_dictionary.VariableDictionary())
		lexer.lex()