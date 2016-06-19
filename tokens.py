'''

The file containing all the tokens used by the LOGIC interpreter.

'''

# Token object for hardcoded values
class Token:
    def __init__(self, show_name, identifier, uses_regex, has_function, expected_arguments):
        self.SHOW_NAME = show_name
        self.IDENTIFIER = identifier
        self.USES_REGEX = uses_regex
        self.has_function = has_function
        self.EXPECTED_ARGUMENTS = expected_arguments

    def to_string(self):
        return "<" + self.SHOW_NAME + ">"

    def is_block(self):
        return self.SHOW_NAME == "BLOCK"

    def is_variable(self):
        return self.SHOW_NAME == "VARIABLE"

    def is_value(self):
        return self.SHOW_NAME == "VALUE"

# Token data object for wrapping the Token object with dynamic data
class TokenData:
    def __init__(self, token):
        self.TOKEN = token
        self.arguments = []
        self.block = []

    def to_string(self):
        string = "{<" + self.TOKEN.SHOW_NAME + " "
        if len(self.arguments) > 0:
            string += "- "
            for argument in self.arguments:
                string += argument + " "
        if len(self.block) > 0:
            string += "- {"
            for token_data in self.block:
                string += "" + token_data.to_string()
            string += "}"
        return string.strip() + ">"

tokens = [
    Token("ECHO", "ECHO(<SPACE>|<EOL>)", True, True, [["VALUE", 0, "+"]]),
    Token("SET", "SET(<SPACE>|<EOL>)", True, True, [["VARIABLE", 1, "."], ["VALUE", 1, "+"]]),

    Token("BLOCK", "{?(\s|\S)*}", True, False, False),
    Token("VARIABLE", "\$[a-zA-Z0-9_]+(<SPACE>|<EOL>)", True, False, False),
    Token("VALUE", "[01]+(<SPACE>|<EOL>)", True, False, False),

    Token("LINE_COMMENT", "#.*<EOL>", True, False, False),

    Token("END_OF_LINE", "<EOL>", False, False, False),
    Token("WHITESPACE", "<SPACE>", True, False, False),
]

