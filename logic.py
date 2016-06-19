'''

The LOGIC interpreter
Written by Oliver S. Neven, in 2016


Use this program to execute LOGIC programs (.lg files)
Example use:
    python3 ./logic.py test.lg

'''

import argparse, re, copy
from tokens import tokens

# Parses and returns launch arguments
def setup_argparse():
    parser = argparse.ArgumentParser(description="The LOGIC interpreter.\nUsed for executing LOGIC programs.")
    parser.add_argument("-f", "--file", help="the LOGIC program to execute", required=True)
    return parser.parse_args()

# Returns a file object in read mode from the pathname
def get_file(pathname):
    try:
        return open(pathname, "r")
    except Exception as e:
        print ("ERROR: Failed to open the file", pathname, "\nReason:", e)
        exit (404)

# Creates a list of tokens from the string for parsing
def tokenize_text(raw_text):
    block = []
    raw_chunk = ""
    for char in raw_text:
        raw_chunk += char
        print ("'", raw_chunk, "'")
        if len(raw_chunk.strip()) > 5 and raw_chunk.strip()[-5:] == "<EOF>":
            print ("ERROR: Unknown token before end of file")
            exit(404)

        for token in tokens:
            if (token.USES_REGEX and re.match(token.IDENTIFIER, raw_chunk.strip()) is not None) or (not token.USES_REGEX and raw_chunk.strip() == token.IDENTIFIER):

                print ("Found a", token.SHOW_NAME, "token!")
                token = copy.copy(token)

                if token.is_block():
                    block = tokenize_text(raw_chunk[1:-1])
                    token.block += block

                if token.EXPECTED_ARGUMENTS is not None:
                    pass
                else:
                    block.append(token)
                raw_chunk = ""
    return block



args = setup_argparse()
file = get_file(args.file)
block = tokenize_text(re.sub(r"\s+", " ", file.read().replace("\n", "<EOL>"))+"<EOL><EOF>")
print ("\nThe following tokens were found:")
for token in block:
    print (token.to_string())



