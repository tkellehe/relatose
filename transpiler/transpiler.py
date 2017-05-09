# -*- coding: UTF-8 -*-
import re

Extendable = type('Extendable', (object,), {})

def REGEXIFY(rstring):
    return re.compile(u"^" + rstring + u"$")

##########################################################################################
# A class that represents a single symbol recognized that holds meaning within a token.
class Symbol:
    #-------------------------------------------------------------------------------------
    # Constructor.
    def __init__(self, token, captured, start, end):
        self.props = Extendable()
        self.token = token
        self.value = captured
        self.start = start
        self.end = end

##########################################################################################
# The main work horse for transpiling. Creates an easy way to access the different
# parts from a regular expression.
class Token:
    #-------------------------------------------------------------------------------------
    # Constructor.
    def __init__(self, match, code, start, end):
        self.props = Extendable()
        # Named groups.
        self.symbols = dict()
        # Un-named groups.
        self.params = []
        # The code that is being interpreted.
        self.code = code
        # The starting and ending location within the code where this token lies.
        self.start = start
        self.end = end
        # What was actually captured.
        self.captured = match.group(0)
        # Represents what the token "literally" is.
        self.literal = None
        # The index within the set of tokens this parse produced.
        self.index = None
        # The snippet object in charge of creating and maintaining this token.
        self.snippet = None
        # The executable that represents a block of tokens.
        self.executable = None

        # Now, loop through and collect all of the symbols (named groups).
        groupnames = match.groupdict()
        for name in groupnames:
            # If is literal, cache it as the attribute literal.
            if name == "literal":
                self.literal = Symbol(self,
                                      match.group("literal"),
                                      match.start("literal"),
                                      match.end("literal"))
            # All others get mapped under the symbols dict.
            elif match.group(name) != None:
                self.symbols[name] = Symbol(self,
                                      match.group(name),
                                      match.start(name),
                                      match.end(name))
            # If not present, set it to None.
            else:
                self.symbols[name] = None
        # Now get the params.
        for param in range(0, len(match.groups())):
            param += 1
            ignore = False
            # Make sure have not already accounted for it in the groupnames.
            for name in groupnames:
                if match.group(name) != None and match.start(param) == match.start(name):
                    ignore = True
                    break
            if not ignore:
                self.params.append(Symbol(self,
                                          match.group(param),
                                          match.start(param),
                                          match.end(param)))
    #-------------------------------------------------------------------------------------
    # A function which will be invoked after everything has been parsed.
    def translate(self):
        pass

##########################################################################################
# A class that handles looking for when to create a particular Token object.
class Snippet:
    #-------------------------------------------------------------------------------------
    # Constructor.
    def __init__(self, regex, tokenize = None):
        self.props = Extendable()
        self.regex = regex
        self.script = None
        # A function that if returns False will reject the Snippets regex.
        # Also, here is where any extra parsing can take place to handle complicated
        # loops.
        self.tokenize = self.donothing if tokenize == None else tokenize
    #-------------------------------------------------------------------------------------
    # The actual function that applies the regex then the traverse function for the
    # final say.
    def parse(self, code, start, end):
        match = self.regex.match(code[start:end])
        if(match != None):
            token = Token(match, code, start, end)
            token.snippet = self
            r = self.tokenize(token)
            # If the result is None or True, return the token else return None.
            return token if r == None or r == True else None
        # Returning None implies it could not create the token based off of the code.
        return None
    #-------------------------------------------------------------------------------------
    # A do nothing function that is used by default when traversing.
    def donothing(self, token):
        pass

##########################################################################################
# A representation of a script.
class Executable:
    #-------------------------------------------------------------------------------------
    # Constructor.
    def __init__(self, script, code):
        self.props = Extendable()
        self.script = script
        self.code = code
        self.tokens = []

##########################################################################################
# Is the actual parser that will generate the Tokens.
class Parser:
    #-------------------------------------------------------------------------------------
    # Constructor.
    def __init__(self):
        self.props = Extendable()
        self.snippets = []
    #-------------------------------------------------------------------------------------
    # Add snippet objects that will be used when parsing the code.
    def add(self, snippet):
        snippet.script = self
        self.snippets.append(snippet)
    #-------------------------------------------------------------------------------------
    # Attempt to create a set of tokens based off of the code provided.
    def parse_left_to_right(self, code):
        executable = Executable(self, code)
        index = 0
        # This code is based off of the concept that whoever can make the
        # most sense out of the code most code, should be the one to
        # get its token selected.
        while index < len(code):
            end = index
            tkn = None
            while end < len(code):
                for snippet in self.snippets:
                    temp = snippet.parse(code, index, end+1)
                    if tkn == None:
                        tkn = temp
                    elif temp != None:
                        tkn = temp
                end += 1

            # Selected the token that makes the most sense out of the most characters.
            # Now can place onto the list of tokens.
            if tkn != None:
                tkn.executable = executable
                tkn.index = len(executable.tokens)
                self.tokens.append(tkn)
                index = tkn.end
            else:
                index += 1

        # All of the tokens now have been packed.
        for tkn in self.tokens:
            tkn.translate(tkn)
    
