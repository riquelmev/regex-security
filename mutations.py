# Mutation functions for the genetic algorithm 
# Jan 2022

import re
import time
import random
import statistics
import root_pb2

import config 
from timing import match_time



def single_char_mutate(string, characters, iterations):
    """
    Changes "iterations" number of characters to random other characters 
    """
    new_string = list(string)
    for i in range(iterations):
        string_index = random.randint(0, len(string) - 1)
        char_index = random.randint(0, len(characters) - 1)
        new_string[string_index] = characters[char_index]
    if len(new_string) > config.max_len:
        new_string = new_string[:config.max_len]
    new_string = "".join(new_string)
    return new_string



def mult_mutate(string, characters):
    """
    Randomly mutates the given string in one of 5 ways, as described in the paper
    """
    new_string = list(string)
    choice = random.choice([1,2,3,4,5])
    char_index = random.randint(0, len(characters) - 1)
    string_index = random.randint(0, len(string) - 1)
    string_index2 = random.randint(0, len(string) - 1)
    if string_index > string_index2:
        string_index, string_index2 = string_index2, string_index
    if choice == 1:
        new_string.append(characters[char_index])
    elif choice == 2:
        new_string = new_string[0:string_index] + list(characters[char_index]) + new_string[string_index:]
    elif choice == 3:
        new_string = new_string[0:string_index] + new_string[string_index2:]
    elif choice == 4:
        new_string = new_string[0:string_index] + new_string[string_index:string_index2] + new_string[string_index:string_index2] + new_string[string_index2:]
    else:
        new_string = new_string[0:string_index] + new_string[string_index:string_index2][::-1] + new_string[string_index2:]
    if len(new_string) > config.max_len:
        new_string = new_string[:config.max_len]
    new_string = "".join(new_string)
    if len(new_string) > 3:
        return new_string
    #TODO
    else:
        return string



def crossover_mutate(input_string, input_string_2):
    """
    Crosses over two strings 
    """
    input_string_copy = list(input_string)
    input_string_copy_2 = list(input_string_2)
    string_index1 = random.randint(0, len(input_string) - 1)
    string_index2 = random.randint(0, len(input_string) - 1)
    if string_index1 > string_index2:
        string_index1, string_index2 = string_index2, string_index1
    input_string_copy = input_string_copy[string_index1:] + input_string_copy_2[string_index2:]
    input_string_copy_2 = input_string_copy_2[string_index1:] + input_string_copy[string_index2:]
    input_string_copy = "".join(input_string_copy)
    input_string_copy_2 = "".join(input_string_copy_2)
    if len(input_string_copy) > config.max_len:
        input_string_copy = input_string_copy[:config.max_len]
    if len(input_string_copy_2) > config.max_len:
        input_string_copy_2 = input_string_copy_2[:config.max_len]
        #TODO
    if len(input_string_copy) < 3:
        input_string_copy = input_string
    if len(input_string_copy_2) < 3:
        input_string_copy_2 = input_string_2
    return input_string_copy, input_string_copy_2



def trim_mutate(regex, input):
    """
    Mutate by removing a character 
    """
    trim = list(input)
    slowest_string = input
    slowest_so_far = 0

    for i in range(1,len(input)-2):
        prime = trim[0:i-1] + trim[i+1:]
        if prime != '':
            prime = "".join(prime)
            time_taken_prime = match_time(regex,prime)[1]
            if time_taken_prime >= slowest_so_far:
                slowest_so_far = time_taken_prime
                slowest_string = prime
    if len(slowest_string) < 3:
        return input
    return slowest_string