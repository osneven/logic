'''

The file containing all the tokens used by the LOGIC interpreter.

'''

class Token:
    SHOW_NAME = None
    IDENTIFIER = None
    USES_REGEX = False
    EXEC = None
    EXPECTED_ARGUMENTS = None
    block = []
    arguments = []

    def __init__(self, show_name, identifier, uses_regex, function, expected_arguments):
        self.SHOW_NAME = show_name
        self.IDENTIFIER = identifier
        self.USES_REGEX = uses_regex
        self.EXEC = function
        self.EXPECTED_ARGUMENTS = expected_arguments

    def to_string(self):
        string = "<" + self.SHOW_NAME + " "

        if len(self.arguments) > 0:
            string += "- "
            for argument in self.arguments:
                string += argument + " "
        if len(self.block) > 0:
            string += "- { "
            for token in self.block:
                string += token.SHOW_NAME + " "
            string += "} "

        return string.strip() + ">"

    def is_block(self):
        return self.SHOW_NAME == "BLOCK"


tokens = [
    Token("BLOCK", "{?(\s|\S)*}", True, None, None),

    Token("LINE_COMMENT", "#.*<EOL>", True, None, None),

    Token("END_OF_LINE", "<EOL>", False, None, None)
]

