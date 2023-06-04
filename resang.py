import sys

def PANIC(msg):
    print(msg)
    exit(1)


# taking care of input
if(len(sys.argv) < 2):
    PANIC("[Error] no file given")

fileName = sys.argv[1]
lines = []
with open(fileName,"r") as f:
    for line in f:
        lines.append(line.strip())


def is_number(char):
    return  "0" <= char  and char <= "9"
def end(list):
    return len(list) == 0
def shift_list(list):
    if(len(list) > 1):
        list = list[1:]
    else:
        list = [] 
    return list


TokensTypes = {
    "(" : "Opara",
    ")" : "Cpara",
    "[" : "OBara",
    "]" : "CBara",
    "," : "Comma",
    "number": "Number",
}
skipableChar = [" ", "\n", "\t"]
class Token:
    def __init__(self,type,value = ""):
        self.value = value
        self.type = type

class Stmt:
    def __init__(self,type):
        self.type = type
class SeriesExpr(Stmt):
    def __init__(self, rhs = None, lhs = None):
        super().__init__("SeriesExpr")    
        self.rhs = rhs
        self.lhs = lhs
class ParallelExpr(Stmt):
    def __init__(self, lhs= None,rhs= None):
        super().__init__("ParallelExpr")    
        self.rhs = rhs
        self.lhs = lhs        
class ProgramExpr(Stmt):
    def __init__(self):
        super().__init__("ProgramExpr")    
        self.body = []
class NumberLiteral(Stmt):
    def __init__(self,value):
        super().__init__("NumberLiteral")    
        self.value = value


def print_ast(ast,depth):
    if(ast == None):
        return
    print("   " * depth,ast.type,ast.value if ast.type == "NumberLiteral" else "")
    if(ast.type == "ProgramExpr"):
        for child in ast.body:
            print_ast(child,depth+1)
    elif (ast.type == "SeriesExpr" or ast.type == "ParallelExpr"):
        print_ast(ast.lhs,depth+1)
        print_ast(ast.rhs,depth+1)
def tokenize(line : str) -> list:
    tokens = []
    line = [char for char in line]
    while(not end(line)):
        char = line[0]
        line = shift_list(line)
        if(char in TokensTypes):
            tokens.append(Token(TokensTypes[char],char))
        elif(is_number(char)):
            x = char
            while(not end(line) and is_number(line[0])):
                char = line[0]
                x += char
                line = shift_list(line)
            tokens.append(Token(TokensTypes["number"],x))
        elif char not  in skipableChar:
            PANIC(f"char {char} not recognized")

    return tokens
class Parser:
    def __init__(self):
        self.tokens =[]    
    def at(self):
        return self.tokens[0]
    def shift(self):
        tkn = self.at()
        if(len(self.tokens) > 1):
            self.tokens = self.tokens[1:]
        else:
            self.tokens = [] 
        return tkn
    def expect(self,type):
        tkn = self.shift()
        if(tkn.type != type):
            PANIC(f"[Error] token mismatch expected {type} got {tkn.type}")
        return tkn
    


    def parse_expr(self):
        return self.parse_serie_expr()
    
    def parse_serie_expr(self):
        lhs = self.parse_primary_expr() 
        while(not end(self.tokens) and self.at().type == TokensTypes[","]):
            self.shift()
            rhs = self.parse_primary_expr()
            lhs = SeriesExpr(
                lhs = lhs,
                rhs = rhs
            )
        return lhs
        
    
    def parse_parallel_expr(self):
        lhs = self.parse_primary_expr() 
        while(not end(self.tokens) and self.at().type == TokensTypes[","]):
            self.shift()
            rhs = self.parse_primary_expr()
            lhs = ParallelExpr(
                lhs = lhs,
                rhs = rhs
            )
        return lhs

    def parse_primary_expr(self):
        tkn =  self.at() 
        expr = ""
        if(tkn.type == TokensTypes["("]):
            self.shift()
            expr = self.parse_serie_expr()
            self.expect(TokensTypes[")"])
        elif(tkn.type == TokensTypes["["]):
            self.shift()
            expr = self.parse_parallel_expr()
            self.expect(TokensTypes["]"])
        elif(tkn.type == TokensTypes["number"]):
            expr = NumberLiteral(int(self.shift().value))
        else:
            PANIC(f"[Error] Unexpexted Expr {tkn.type} {tkn.value}")

        return expr

    def parse(self,tokens):
        self.tokens = tokens
        program = ProgramExpr()
        while(not end(self.tokens)):
            program.body.append(self.parse_expr())
        return program
class Interpreter:
    def __init__(self):
        pass

    def eval_serie(self,ast):
        lhs = self.eval(ast.lhs)
        rhs = self.eval(ast.rhs)
        return lhs + rhs
    def eval_parallel(self,ast):
        lhs = self.eval(ast.lhs)
        rhs = self.eval(ast.rhs)
        return 1/(1/lhs + 1/rhs)
    def eval_program(self,ast):
        last_evaluated   = None
        for child in ast.body:
            last_evaluated = self.eval(child)
        return last_evaluated
    def eval(self,ast):
        if ast.type == "ProgramExpr":
            return self.eval_program(ast)
        elif ast.type == "SeriesExpr":
            return self.eval_serie(ast)       
        elif ast.type == "ParallelExpr":
            return self.eval_parallel(ast)  
        elif ast.type == "NumberLiteral":
            return ast.value
        else:
            PANIC("[Error] Expr eval not implemented")   


    



parser = Parser()
ast = parser.parse(list(tokenize(lines[0])))
interpreter = Interpreter()
output = interpreter.eval(ast)
print(output)