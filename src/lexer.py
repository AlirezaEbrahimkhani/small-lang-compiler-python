class Lexer:
    
     # Define all regex
    RE_KEYWORD = "var|const|if|then|begin|end|integer|procedure|in|out|in out|print|read|for|to|do|return|call|not|and|or|else|string|bool"
    RE_IDENTIFIER = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    RE_NUMERAL = "[.0-9]"
    RE_OPERATOR = "(=)|(:=)|(<=)|(>=)|(>)|(<)|(<>)|(-)|(\+)|(/)|(\*)"
    RE_SPCIAL_CHARACTERS = "[$&+,:;=?@#|'<>.^*()%!-]"
    
    def __init__(self , source_code):
        self.source_code = source_code
    
    # This method reads a character and reads the word to the end and recognizes the token
    def _scan(self ,first_char ,chars ,allowed):
        
        ret = first_char
        p = chars.next
        while p is not None and re.match(allowed, p):
            
            ret += chars.move_next()
            p = chars.next
            
        if(re.match(self.RE_KEYWORD , ret)):
            return("KEYWORD" , ret)
        
        elif(re.match(self.RE_IDENTIFIER ,ret)):
            return("IDENTIFIER" , ret)
        
        elif(re.match(self.RE_NUMERAL , ret)):
            return("NUMERAL" , ret)
        
        elif(re.match(self.RE_OPERATOR , ret)):
            if(re.match(self.RE_NUMERAL , p)):
                ret += chars.move_next()
                p = chars.next
                p = ""
                return ("NUMERAL" , ret + p)
            else:
                return("OPERATOR" , ret)
        
        elif (re.match(self.RE_SPCIAL_CHARACTERS , ret)):
            return("SPECIAL_CHARACTER" , ret)

    # Read characters one by one
    def lex(self):

        chars = PeekableStream(self.source_code)
        while chars.next is not None:
            
            c = chars.move_next()
            
            if c in " \n":
                pass
            
            elif re.match(self.RE_SPCIAL_CHARACTERS , c):
                yield (self._scan(c,  chars , self.RE_SPCIAL_CHARACTERS))
                
            elif re.match(self.RE_OPERATOR , c):
                yield (self._scan(c,  chars , self.RE_OPERATOR))
                
            elif re.match(self.RE_NUMERAL , c):                     
                yield (self._scan(c, chars, self.RE_NUMERAL))
                
            elif re.match(self.RE_IDENTIFIER , c):   
                yield (self._scan(c, chars, self.RE_IDENTIFIER))