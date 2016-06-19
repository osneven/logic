'''

The file containing all the tokens used by the LOGIC interpreter.

'''

# Token object for hardcoded values
class Token:
    def __init__(self, show_name, identifier, uses_regex, function, expected_arguments):
        self.SHOW_NAME = show_name
        self.IDENTIFIER = identifier
        self.USES_REGEX = uses_regex
        self.EXEC = function
        self.EXPECTED_ARGUMENTS = expected_arguments

    def to_string(self):
        return "<" + self.SHOW_NAME + ">"

    def is_block(self):
        return self.SHOW_NAME == "BLOCK"

    def is_tag(self):
        return self.IDENTIFIER == "<EOF>" or self.IDENTIFIER == "<EOL>"

# Token data object for wrapping the Token object with dynamic data
class TokenData:
    def __init__(self, token):
        self.TOKEN = token
        self.arguments = []
        self.block = []

    def to_string(self):
        if self.TOKEN.is_tag():
            return ""

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
    Token("ECHO", "ECHO", False, )
    Token("BLOCK", "{?(\s|\S)*}", True, None, None),
    Token("LINE_COMMENT", "#.*<EOL>", True, None, None),
    Token("END_OF_LINE", "<EOL>", False, None, None)
]

