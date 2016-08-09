'''

	The LOGIC interpreter
	Author: Oliver S. Neven
	Written in 2016

	This python program is used to execute LOGIC programs  and .logic files
	For executing a .logic file run:
		python ./logic.py path/to/file.logic

'''

import sys, tokenizer, lexer, os, variable_dictionary, argparse

# Parses arguments
def parse_args():
	parser = argparse.ArgumentParser(description='This is the LOGIC interpreter, used for running LOGIC program files.')
	parser.add_argument('file', action='store', help='the LOGIC file to run')
	parser.add_argument('-d', '--debug', action='store_true', help='prints debug information')
	return parser.parse_args()

# Run this with parsed arguments
def run_logic_interpreter(args):

	# Create a block of tokenized code from the file
	if args.debug: print ('\n---------- Tokenizing ----------\n')
	file = open(args.file, 'r')
	raw_code = file.read()
	block = tokenizer.tokenize(raw_code, args.debug)

	# Parse the block
	if args.debug: print ('\n----------  Parsing  -----------\n')
	lex = lexer.Lexer(block, variable_dictionary.VariableDictionary())
	lex.lex(args.debug)

try:
	parsed_args = parse_args()
	run_logic_interpreter(parsed_args)
except KeyboardInterrupt:
	sys.exit()

