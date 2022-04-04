# functions related to seeding the genetic algorithm 
# Jan 2022

import random
import config
import string as String 
import root_pb2 as root



def get_tokens(regex):
    """
    extract the literals from a given regex
    return: a list of single-character strings 
    """
    tokens = [] 
    for t in regex.tokens:
        if t.type == root.TokenType.Character and t.token != "":
            if t.token[0] == "\\":      # remove the escape \
                tokens.append(t.token[1:])
            else:
                tokens.append(t.token)
    return tokens



def regex_substrings(tokens):
    """
    input a list of characters 
    output all the substrings 
    abc -> a, b, c, ab, bc, abc
    """
    seeds = [] 
    for i in range(len(tokens)):
        for j in range(i, len(tokens)+1):
            substring = "".join(tokens[i:j])
            seeds.append(substring)
    return seeds 



def generate_seeds(tokens):
    """
    input tokens, a list of characters to be randomly (uniformly) sampled into strings 
    takes in list of tokens as single-character strings 
    """

    # get list of characters (alphabet, digits, punctuation)
    chars = String.printable
    if len(tokens)>0:
        substrings = regex_substrings(tokens) 
    else: 
        substrings = String.printable 

    seeds = []
    for i in range(config.num_seeds):
        length = random.randrange(2, config.max_len)
        seed = ""
        for j in range(length):
            # 50% pick character from substrings, 50% pick from chars 
            char = random.choice(random.choice([substrings, chars]))
            seed = seed + char     
        seeds.append(seed)
    return seeds 