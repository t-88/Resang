import sys

# taking care of input
if(len(sys.argv) < 2):
    print("[Error] no file given")
    exit(1)

fileName = sys.argv[1]
lines = []
with open(fileName,"r") as f:
    for line in f:
        lines.append(line.strip())


def is_number(char):
    return  "0" <= char  and char <= "9"
# end of line
def eol(line):
    return len(line) == 0

def shift(line):
    if(len(line) > 1):
        line = line[1:]
    else:
        line = "" 
    return line


TokensTypes = {
    ")" : "Opara",
    "(" : "Cpara",
    "[" : "OBara",
    "]" : "CBara",
    "," : "Comma",
    "number": "Number",
}
class Token:
    def __init__(self,type,value = ""):
        self.value = value
        self.type = type



def tokenize(line) -> list:
    tokens = []
    line = [char for char in line]
    while(not eol(line)):
        char = line[0]
        line = shift(line)
        if(char in TokensTypes):
            tokens.append(Token(TokensTypes[char],char))
        elif(is_number(char)):
            x = char
            while(not eol(line) and is_number(line[0])):
                char = line[0]
                x += char
                line = shift(line)
            tokens.append(Token(TokensTypes["number"],x))

    return tokens


tokens = tokenize(lines[0])
for token in tokens:
    print(token.type,":",token.value)