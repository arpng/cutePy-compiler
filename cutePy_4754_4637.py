# Name:Aristeidis Panagiotou    AM:4754     username:cse94754
# Name:Ilias Varthalitis    AM:4637     username:cse94637

import sys


if len(sys.argv) != 2:
    print("Wrong arguments given, correct usage is cutePy_4754_4637.py TEST_FILE_NAME.cpy")
    exit()

f = open(sys.argv[1], "r")


#f = open("test2.cpy", "r") #use this in vscode

class Token():    ## class Token for the returned token
    def __init__(self, recognized_string, family, line_number):  # init function for class Token
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return f'family:{self.family}, recognized_string: {self.recognized_string},line_number: {self.line_number})'


class Lex:  ## class Lex for lexical analyzer
    def __init__(self):
        self.line_number = 1       ## line_number from the file starts at 1
        self.input_file = f.read(1)   ## the first read from the file  

    def next_token(self):    ## A function for taking the next token every time 
        output_string  = ''     ## We add to the output_string every letter and we return that
        output_temp = ''        ## A temporary string to holds the letters for identifiers
        whitespace_array = [' ', '\t', '\n']   ## array for whitespaces
        state = "start"   ## we begin from the "start"
        loop_array = ["invalid symbol", "Error, EOF reached comment never closed", "Error, #declare expected", "Error, '#{' or '#declare' or '#$' expected", "Error, '!=' expected", "Error, EOF reached", "number", "identifier" ,"keyword" ,"Declaration","logic_symbol" ,"add_Operator" ,"mul_Operator" ,"group_Symbol" ,"delimeter" ,"rel_Operator" ,"Assignment","Error, '//' expected", "declare", "comment"]
        keyword_array = ['if','while','def','else' ,'return' ,'print' , 'input', 'int' ,'__name__' , '"__main__"']
        logic_array = ['and' , 'or', 'not']
        valid_symbols = ["_", "+", "-", "*", "//", "<", ">", "!=", "<=", ">=", "==", "=", ";", ",", ":", "[", "]",
                         "(", ")", "#{", "#}", "#$"]
        
        while(state not in loop_array):    ## the while loop stops every time we see a terminal symbol
            if(self.input_file == "\n"):
                self.line_number += 1
            if(self.input_file == ''):  #EOF reached
                output_string = ''
                state = "Error, EOF reached"
            if(state=="start" and self.input_file in whitespace_array):  #use isspace() alternatively
                self.input_file = f.read(1)
            
            if(state=="start" and self.input_file.isnumeric()):
                state = "digit"

            elif(state=="start" and (self.input_file.isalpha() or self.input_file == "_" or self.input_file == '"')):    #check only self.input_file[i(or 0 but i should always be 0)] cuz an identifier can have numbers in it
                state = "idk"
                output_temp += self.input_file
                
            elif(state=="start" and (self.input_file == "+" or self.input_file == "-")):
                state = "add_Operator"
                output_string  += self.input_file
                self.input_file = f.read(1)

            elif(state=="start" and self.input_file == "/"):
                state = "div_temp"

            elif(state=="start" and self.input_file == "*"):
                state = "mul_Operator"
                output_string  += self.input_file
                self.input_file = f.read(1)
                
            elif(state=="start" and (self.input_file == "[" or self.input_file == "]" or self.input_file == "(" or self.input_file == ")" )):
                state = "group_Symbol"
                output_string  += self.input_file
                self.input_file = f.read(1)

            elif(state=="start" and (self.input_file == ";" or self.input_file == "," or self.input_file == ":" )): 
                state = "delimeter"
                output_string  += self.input_file
                self.input_file = f.read(1)  

            elif(state=="start" and (self.input_file == "<" or self.input_file == ">" )):
                state = "rel_temp"
                
            elif(state=="start" and self.input_file == "!"):
                state = "different"
                    
            elif(state=="start" and self.input_file == "#"):
                state = "group_or_comment"
                    
            elif(state=="start" and self.input_file == "="):
                state = "rel_assignment_temp"
            
            elif(state == "start" and self.input_file not in valid_symbols and self.input_file not in whitespace_array):
                output_string  += self.input_file
                state = "invalid symbol"
                self.input_file = f.read(1)
            #############################################################################################################################
            if (state == "digit"):
                output_string  += self.input_file
                self.input_file = f.read(1)
                if(self.input_file.isnumeric()):
                    state = "digit"  
                else:
                    state = "number"
            
            if(state == "idk"):
                output_string  += self.input_file
                self.input_file = f.read(1)
                if((self.input_file.isalpha() or self.input_file.isnumeric() or self.input_file == "_" or self.input_file == '"')):
                    state = "idk"
                    output_temp += self.input_file
                else:
                    if(output_temp in keyword_array):
                        state = "keyword"
                    elif(output_temp in logic_array):
                        state = "logic_symbol"
                    else:
                        state = "identifier"
                
            if(state == "div_temp"):
                output_string  += self.input_file
                self.input_file = f.read(1)
                if(self.input_file == "/"):
                    state = "mul_Operator"
                    output_string  += self.input_file
                    self.input_file = f.read(1)
                else:
                    state = "Error, '//' expected"
            
            if(state == "different"):
                output_string  += self.input_file
                self.input_file = f.read(1)
                if(self.input_file == "="): 
                    state = "rel_Operator"
                    output_string  += self.input_file
                    self.input_file = f.read(1)
                else:
                    state = "Error, '!=' expected"
            
            if(state == "group_or_comment"):
                self.input_file = f.read(1)
                if(self.input_file == "{" or self.input_file == "}"):
                    state = "group_Symbol"
                    output_string  += "#"+self.input_file
                    self.input_file = f.read(1)
                elif(self.input_file.isalpha()):
                    state = "dec_temp"
                    output_temp += self.input_file
                elif(self.input_file == "$"):
                    state = "comment_temp"
                else:
                    state = "Error, '#{' or '#declare' or '#$' expected"

            if(state == "dec_temp"):
                self.input_file = f.read(1)
                if(self.input_file.isalpha()):
                    state = "dec_temp"
                    output_temp += self.input_file
                else:
                    if(output_temp == "declare"):
                        state = "Declaration"
                        output_string  = "#" + output_temp
                    else:
                        state = "Error, #declare expected"
                        output_string  = output_temp


            if(state == "comment_temp"):
                self.input_file = f.read(1)
                if(self.input_file == "#"):
                    state = "comment_temp2"
                elif(self.input_file == ''):  #  EOF
                    state = "Error, EOF reached comment never closed"
                    output_string  += self.input_file
                else:
                    state = "comment_temp"

            if(state == "comment_temp2"):
                self.input_file = f.read(1)
                if(self.input_file == "$"):
                    state = "start"
                    self.input_file = f.read(1)
                elif(self.input_file == ''):  #  EOF
                    state = "Error, EOF reached comment never closed"
                    output_string  += self.input_file
                else:
                    state = "comment_temp"
            
            if(state == "rel_assignment_temp"):
                output_string  += self.input_file
                self.input_file = f.read(1)
                if(self.input_file == "="):
                    state = "rel_Operator"
                    output_string  += self.input_file
                    self.input_file = f.read(1)
                else:
                    state = "Assignment"
                    self.input_file = f.read(1)

            if(state == "rel_temp"):
                output_string  += self.input_file
                self.input_file = f.read(1)
                if(self.input_file == "="):
                    state = "rel_Operator"
                    output_string  += self.input_file
                    self.input_file = f.read(1)
                else:
                    state = "rel_Operator"    
        
        token = Token(output_string , state, self.line_number)
        return token


class Parser():
    def __init__(self):
        self.lexical_analyzer = Lex()
        self.token = Token("", "start", 1)
    
    def syntax_analyzer(self):
    
        if(self.startRule()):
            print("Compilation successfully completed")
        else:
            print("Compilation failed")
        
        

    def startRule(self):
        self.token = self.lexical_analyzer.next_token()
        if(self.def_main_part() and self.call_main_part()): 
            return True
        else:
            return False

    def def_main_part(self):
        if(self.def_main_function()):
            while(self.def_main_function()):
                continue
            return True
        else:
            return False

    def def_main_function(self):
        if(self.token.recognized_string == "def"):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.family == "identifier"):
                self.token = self.lexical_analyzer.next_token()
                if(self.token.recognized_string == "("):
                    self.token = self.lexical_analyzer.next_token()
                    if(self.token.recognized_string == ")"):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == ":"):
                            self.token = self.lexical_analyzer.next_token()
                            if(self.token.recognized_string == "#{"):
                                self.token = self.lexical_analyzer.next_token()
                                self.declarations()
                                while(self.def_function()):
                                    continue
                                if(self.statements()):
                                    if(self.token.recognized_string == "#}"):
                                        self.token = self.lexical_analyzer.next_token()
                                        return True
                                    else:
                                        self.error("#}")
                                        print("Compilation failed")
                                        exit()
                                else:
                                    return False
                            else:
                                self.error("#{")
                                return False
                        else:
                            self.error(":")
                            print("Compilation failed")
                            exit()
                    else:
                        self.error(")")
                        return False
                else:
                    self.error("(")
                    return False
            else:
                self.error("identifier")
                return False
        else:
            if(self.token.family == "identifier" or self.token.recognized_string == "#{" or self.token.family == "keyword"):
                return False
            else:
                self.error("def")
                return False                                                                   

    def def_function(self):
        if(self.token.recognized_string == "def"):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.family == "identifier"):
                self.token = self.lexical_analyzer.next_token()
                if(self.token.recognized_string == "("):
                    self.token = self.lexical_analyzer.next_token()
                    self.id_list()
                    if(self.token.recognized_string == ")"):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == ":"):
                            self.token = self.lexical_analyzer.next_token()
                            if(self.token.recognized_string == "#{"):
                                self.token = self.lexical_analyzer.next_token()
                                self.declarations()
                                while(self.def_function()):
                                    continue
                                if(self.statements()):
                                    if(self.token.recognized_string == "#}"):
                                        self.token = self.lexical_analyzer.next_token()
                                        return True
                                    else:
                                        self.error("#}")
                                        print("Compilation failed")
                                        exit()
                                else:
                                    return False
                            else:
                                self.error("#{")
                                print("Compilation failed")
                                exit()
                        else:
                            self.error(":")
                            print("Compilation failed")
                            exit()
                    else:
                        self.error(")")
                        return False
                else:
                    self.error("(")
                    return False
            else:
                self.error("identifier")
                return False
        else:
            if(self.token.family == "identifier" or self.token.recognized_string == "#{" or self.token.family == "keyword"):
                return False
            else:
                self.error("def")
                return False   

    def declarations(self):
        while(self.declaration_line()):
            continue

    def declaration_line(self):
        if(self.token.recognized_string == "#declare"): 
            self.token = self.lexical_analyzer.next_token()
            if(self.id_list()):
                return True
            else:
                return False
        else:
            return False

    def statement(self):
        if(self.simple_statement()):
            return True
        elif(self.structured_statement()):
            return True
        else:
            return False

    def statements(self):
        if(self.statement()):
            while(self.statement()):
                continue  
            return True 
        else:
            return False   

    def simple_statement(self):
        if(self.assignment_stat()):
            return True
        elif(self.print_stat()):
            return True
        elif(self.return_stat()):
            return True
        else:
            return False

    def structured_statement(self):
        if(self.if_stat()):
            return True
        elif(self.while_stat()):
            return True
        else:
            return False

    def assignment_stat(self):
        if(self.token.family == "identifier"):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == "="):
                self.token = self.lexical_analyzer.next_token()
                if(self.expression()):
                    if(self.token.recognized_string == ";"):
                        self.token = self.lexical_analyzer.next_token()
                        return True
                    else:
                        self.error(self.token.recognized_string)
                        print("Compilation failed")
                        exit()   
                else:     
                    if(self.token.recognized_string == "int"):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == "("):
                            self.token = self.lexical_analyzer.next_token()
                            if(self.token.recognized_string == "input"):
                                self.token = self.lexical_analyzer.next_token()
                                if(self.token.recognized_string == "("):
                                    self.token = self.lexical_analyzer.next_token()
                                    if(self.token.recognized_string == ")"):
                                        self.token = self.lexical_analyzer.next_token()
                                        if(self.token.recognized_string == ")"):
                                            self.token = self.lexical_analyzer.next_token()
                                            if(self.token.recognized_string == ";"):
                                                self.token = self.lexical_analyzer.next_token()
                                                return True
                                            else:
                                                self.error(";")
                                                print("Compilation failed")
                                                exit()
                                        else:
                                            self.error(self.token.recognized_string)
                                            return False
                                    else:
                                        self.error(")")
                                        return False
                                else:
                                    self.error("(")
                                    return False
                            else:
                                self.error("input")
                                return False
                        else:
                            self.error("(")
                            return False
                    else:
                        self.error("int")
                        return False    
            else:
                self.error("=")
                return False
        else:
            return False    

    def print_stat(self):
        if(self.token.recognized_string == "print"):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == "("):
                self.token = self.lexical_analyzer.next_token()
                if(self.expression()):
                    if(self.token.recognized_string == ")"):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == ";"):
                            self.token = self.lexical_analyzer.next_token()
                            return True 
                        else:
                            self.error(";")
                            print("Compilation failed")
                            exit()
                    else:
                        self.error(")")
                        return False
                else:
                    return False
            else:
                self.error("(")
                return False        
        else:
            self.error("print")
            return False
                    
    def return_stat(self):
        if(self.token.recognized_string == "return"):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == "("):
                self.token = self.lexical_analyzer.next_token()
                if(self.expression()):
                    if(self.token.recognized_string == ")"):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == ";"):
                            self.token = self.lexical_analyzer.next_token()
                            return True 
                        else:
                            self.error(";")
                            print("Compilation failed")
                            exit()
                    else:
                        self.error(")")
                        return False
                else:
                    return False
            else:
                self.error("(")
                return False        
        else:
            self.error("return")
            return False

    def if_stat(self):
        if(self.token.recognized_string == 'if'):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == '('):
                self.token = self.lexical_analyzer.next_token()
                if(self.condition()):
                    if(self.token.recognized_string == ')'):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == ':'):
                            self.token = self.lexical_analyzer.next_token()
                            if(self.statement()):
                                if(self.token.recognized_string == 'else'):
                                    self.token = self.lexical_analyzer.next_token()
                                    if(self.token.recognized_string == ':'):
                                        self.token = self.lexical_analyzer.next_token()
                                        if(self.statement()):
                                            return True
                                        else:
                                            if(self.token.recognized_string == '#{'):
                                                self.token = self.lexical_analyzer.next_token()
                                                if(self.statements()):
                                                    if(self.token.recognized_string == '#}'):
                                                        self.token = self.lexical_analyzer.next_token()
                                                        return True
                                                    else:
                                                        self.error('#}')
                                                        print("Compilation failed")
                                                        exit()
                                                else:
                                                    return False
                                            else:
                                                self.error('#{')
                                                return False
                                    else:
                                        self.error(':')
                                        print("Compilation failed")
                                        exit()
                                else:
                                    return True #else not needed so u can return true
                            else:
                                if(self.token.recognized_string == '#{'):
                                    self.token = self.lexical_analyzer.next_token()
                                    if(self.statements()):
                                        if(self.token.recognized_string == '#}'):
                                            self.token = self.lexical_analyzer.next_token()
                                            if(self.token.recognized_string == 'else'):
                                                self.token = self.lexical_analyzer.next_token()
                                                if(self.token.recognized_string == ':'):
                                                    self.token = self.lexical_analyzer.next_token()
                                                    if(self.statement()):
                                                        return True
                                                    else:
                                                        if(self.token.recognized_string == '#{'):
                                                            self.token = self.lexical_analyzer.next_token()
                                                            if(self.statements()):
                                                                if(self.token.recognized_string == '#}'):
                                                                    self.token = self.lexical_analyzer.next_token()
                                                                    return True
                                                                else:
                                                                    self.error(self.token.recognized_string)
                                                                    print("Compilation failed")
                                                                    exit()
                                                            else:
                                                                return False
                                                        else:
                                                            self.error(self.token.recognized_string)
                                                            return False
                                                else:
                                                    self.error(self.token.recognized_string)
                                                    print("Compilation failed")
                                                    exit()
                                            else:
                                                return True #else not needed so u can return true
                                        else:
                                            self.error(self.token.recognized_string)
                                            print("Compilation failed")
                                            exit()
                                    else: 
                                        return False
                                else:
                                    self.error(self.token.recognized_string)
                                    return False
                        else:
                            self.error(':')
                            print("Compilation failed")
                            exit()
                    else:
                        self.error(')')
                        return False
                else:
                    return False
            else:
                self.error('(')
                return False
        else:
            self.error('if')
            return False

    def while_stat(self):
        if(self.token.recognized_string == 'while'):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == '('):
                self.token = self.lexical_analyzer.next_token()
                if(self.condition()):
                    if(self.token.recognized_string == ')'):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == ':'):
                            self.token = self.lexical_analyzer.next_token()
                            if(self.statement()):
                                return True
                            else:
                                if(self.token.recognized_string == '#{'):
                                    self.token = self.lexical_analyzer.next_token()
                                    if(self.statements()):
                                        if(self.token.recognized_string == '#}'):
                                            self.token = self.lexical_analyzer.next_token()
                                            return True
                                        else:
                                            self.error('#}')
                                            print("Compilation failed")
                                            exit()
                                    else:
                                        return False
                                else:
                                    self.error('#{')
                                    return False
                        else:
                            self.error(':')
                            print("Compilation failed")
                            exit()
                    else:
                        self.error(')')
                        return False
                else:
                    return False
            else:
                self.error('(')
                return False
        else:
            if(self.token.recognized_string == "#{" or self.token.recognized_string == "#}"):
                return False
            else:
                self.error('while')
                return False

    def id_list(self):
        if(self.token.family == "identifier"):
            self.token = self.lexical_analyzer.next_token()
            while(self.token.recognized_string == ","):
                self.token = self.lexical_analyzer.next_token()
                if(self.token.family == "identifier"):
                    self.token = self.lexical_analyzer.next_token()
                else:
                    self.error("identifier")
                    return False
            return True
        else:
            return True

    def expression(self):
        if(self.optional_sign() and self.term()):
            while(self.token.family == "add_Operator"):
                self.token = self.lexical_analyzer.next_token()
                if(self.term()):
                    continue
                else:
                    return False
            return True
        else:
            return False

    def term(self):
        if(self.factor()):
            while(self.token.family == "mul_Operator"):
                self.token = self.lexical_analyzer.next_token()
                if(self.factor()):
                    continue
                else:
                    return False
            return True    
        else:
            return False

    def factor(self):
        if(self.token.family == "number"):
            self.token = self.lexical_analyzer.next_token()
            return True
        elif(self.token.recognized_string == '('):
            self.token = self.lexical_analyzer.next_token()
            if(self.expression()):
                if(self.token.recognized_string == ')'):
                    self.token = self.lexical_analyzer.next_token()
                    return True
                else:
                    self.error(")")
                    return False
            else:
                return False
        elif(self.token.family == "identifier"):
            self.token = self.lexical_analyzer.next_token()
            if(self.idtail()):
                return True
            else:
                return False
        else:
            self.error("number or identifier or '(' ")
            return False      
   
    def idtail(self):
        if(self.token.recognized_string == "("):
            self.token = self.lexical_analyzer.next_token()
            if(self.actual_par_list()):
                if(self.token.recognized_string == ")"):
                    self.token = self.lexical_analyzer.next_token()
                    return True
                else:
                    self.error(")")
                    return False
            else:
                return False
        else:
            return True     

    def actual_par_list(self):
        if(self.expression()):
            while(self.token.recognized_string == ","):
                self.token = self.lexical_analyzer.next_token()
                if(self.expression()):
                    continue
                else:
                    return False
            return True
        return True 

    def optional_sign(self):
        if(self.token.family == "add_Operator"):
            self.token = self.lexical_analyzer.next_token()
            return True
        else:
            return True

    def condition(self):
        if(self.bool_term()):
            while(self.token.recognized_string == "or"):
                self.token = self.lexical_analyzer.next_token()
                if(self.bool_term()):
                    continue
                else:
                    return False
            return True
        else:
            return False

    def bool_term(self):
        if(self.bool_factor()):
            while(self.token.recognized_string == "and"):
                self.token = self.lexical_analyzer.next_token()
                if(self.bool_factor()):
                    continue
                else:
                    return False
            return True
        else:
            return False

    def bool_factor(self):
        if(self.token.recognized_string == "not"):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == "["):
                self.token = self.lexical_analyzer.next_token()
                if(self.condition()):
                    if(self.token.recognized_string == "]"):
                        self.token = self.lexical_analyzer.next_token()
                        return True
                    else:
                        self.error("]")
                        return False
                else:
                    return False
            else:
                self.error("[")
                return False               
        elif(self.token.recognized_string == "["):
            self.token = self.lexical_analyzer.next_token()
            if(self.condition()):
                if(self.token.recognized_string == "]"):
                    self.token = self.lexical_analyzer.next_token()
                    return True
                else:
                    self.error("]")
                    return False  
            else:
                return False     
        else:
            if(self.expression()):
                if(self.token.family == "rel_Operator"):
                    self.token = self.lexical_analyzer.next_token()
                    if(self.expression()):
                        return True
                    else:
                        return False
                else:
                    self.error("rel_Operator")
                    return False
            else:
                return False

    def call_main_part(self):
        if(self.token.recognized_string == "if"):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == "__name__"):
                self.token = self.lexical_analyzer.next_token()
                if(self.token.recognized_string == "=="):
                    self.token = self.lexical_analyzer.next_token()
                    if(self.token.recognized_string == '"__main__"'):
                        self.token = self.lexical_analyzer.next_token()
                        if(self.token.recognized_string == ":"):
                            self.token = self.lexical_analyzer.next_token()
                            if(self.main_function_call()):
                                while(self.main_function_call()):
                                    continue
                                return True
                            else:
                                return False    
                        else:
                            self.error(":")
                            print("Compilation failed")
                            exit()
                    else:
                        self.error('"__main__"')
                        return False
                else:
                    self.error("==")
                    return False
            else:
                self.error("__name__")  
                return False      
        else:
            self.error("if")
            return False

    def main_function_call(self):
        if(self.token.recognized_string == ''):
            print("Compilation successfull")
            exit()

        if(self.token.family == 'identifier'):
            self.token = self.lexical_analyzer.next_token()
            if(self.token.recognized_string == '('):
                self.token = self.lexical_analyzer.next_token()
                if(self.token.recognized_string == ')'):
                    self.token = self.lexical_analyzer.next_token()
                    if(self.token.recognized_string == ';'):
                        self.token = self.lexical_analyzer.next_token()
                        return True
                    else:
                        self.error(';')
                        print("Compilation failed")
                        exit()
                else:
                    self.error(';')
                    print("Compilation failed")
                    exit()
            else:
                self.error(';')
                print("Compilation failed")
                exit()
        else:
            self.error(';')
            print("Compilation failed")
            exit() 
    
    def error(self,input_error):
        if(input_error == "def"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == "identifier"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == "("):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == ")"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == ":"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == "#{"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == "#}"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == "while"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == ","):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == "rel_Operator"):
            print(input_error , " expected at line" , self.token.line_number)
        if(input_error == "#declare"):
            print(input_error , " expected at line" , self.token.line_number)



parser = Parser()
parser.syntax_analyzer()