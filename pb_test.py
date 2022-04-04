import os
import root_pb2


e = root_pb2.Expression()
e.ParseFromString(b'x01\x082\x08B\x01)H\x04\x88\x01\x012\x04H\x05r\x002\x08B\x01(H\x04\x88\x01\x002\x08B\x02?=H\x06x\x002\x08B\x01.H\x08\x90\x01\x052\x07B\x01*H\x02`\x012\x04H\x05r\x002\x08B\x01[H\x08\x90\x01\x002\nB\x03a-zH\x08\x90\x01\x042\x08B\x01]H\x08\x90\x01\x012\x08B\x01)H\x04\x88\x01\x012\x04H\x05r\x002\x08B\x01(H\x04\x88\x01\x002\x08B\x02?=H\x06x\x002\x08B\x01.H\x08\x90\x01\x052\x07B\x01*H\x02`\x012\x04H\x05r\x002\x08B\x01[H\x08\x90\x01\x002\nB\x03A-ZH\x08\x90\x01\x042\x08B\x01]H\x08\x90\x01\x012\x08B\x01)H\x04\x88\x01\x012\x04H\x05r\x002\x08B\x01(H\x04\x88\x01\x002\x08B\x02?=H\x06x\x002\x08B\x01.H\x08\x90\x01\x052\x07B\x01*H\x02`\x012\x04H\x05r\x002\x08B\x01[H\x08\x90\x01\x002\nB\x03a-zH\x08\x90\x01\x042\nB\x03A-ZH\x08\x90\x01\x042\x08B\x01]H\x08\x90\x01\x012\x08B\x01)H\x04\x88\x01\x012\x08B\x01.H\x08\x90\x01\x052\x04H\x05r\x002\nB\x04{8,}H\x02`\x022\x07B\x01$H\x03h\x012\x0cB\x03/gmH\x05r\x03/gm')

for tok in e.tokens:
    print(tok)

#print(dir(e))
#print(e.raw)
# char_tokens = [t for t in e.tokens if t.type == TokenType.CharacterClass]
char_tokens = [t for t in e.tokens] #if t.type == 5 or t.type == 8]
for c in char_tokens:
    print(c.token, c.type)
    if c.type == 2 or c.type ==1 :
        print(c.type == root_pb2.TokenType.QuantifierModifier)
        print(c.quantifiermodifier)
    # print(tok.type)
    # if tok.type == 5: # character 
    #     print("->", tok.character)
    # elif tok.type == 8: # characterClass 
    #         # go through individual characterClass types 
    #         if tok.characterclass == 0:
    #             print("[")
    # print("--")


def get_seed_chars(e):
    out = []
    for tok in e.tokens:
        if tok.type == 5: # character 
            print(tok.character)
        elif tok.type == 8: # characterClass 
            # go through individual characterClass types 
            if tok.characterClass == 0:
                print("[")
