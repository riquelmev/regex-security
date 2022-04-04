# Builtin imports
import time
import sys
import base64
from tqdm import tqdm 
import string as String 
import matplotlib.pyplot as plt

# Internal imports
import config
import root_pb2
from mutations import single_char_mutate, mult_mutate, crossover_mutate, trim_mutate
from timing import match_time, match_time, slowest_total_match_time
from seeding import generate_seeds, get_tokens

testing = False    


def cull(regex, generation, number_of_survivors):
    """
    Culls the least desireable inputs
    Only keeps the [number_of_survivors] slowest in the generation 
    """
    dict = {}
    ordered_generation = []
    for input in generation:
        if input != "":
            dict[input] = match_time(regex, input)
    sorted_inputs = sorted(dict.items(), key=lambda kv: kv[1], reverse=True)
    for input in sorted_inputs:
        ordered_generation.append(input[0])
    # Keep slowest
    keepers = ordered_generation[:number_of_survivors]
    return keepers


def pump(regex, input):
    """
    Finds the slowest section of the input and "pumps" it be repeating it in place as many times as possible 
    "xxbadxx" -> "xxbadbadbadbadxx"
    """
    trim = list(input)
    slowest_string = input
    slowest_so_far = 0

    for i in range(1, len(input) - 2):
        prime = trim[0:i - 1] + trim[i + 1:]
        if prime != '':
            prime = "".join(prime)
            time_taken_prime = match_time(regex, prime)
            if time_taken_prime >= slowest_so_far:
                slowest_so_far = time_taken_prime
                slowest_string = prime
    string = slowest_string
    m = 0
    i_star = 0
    j_star = 0
    for i in range(0, len(string) - 1):
        for j in range(i + 1, len(string) - 2):
            prime = string[0:i - 1] + string[i:j] * 2 + string[j + 1:]
            if match_time(regex, prime) >= m:
                m = match_time(regex, prime)
                i_star = i
                j_star = j
    k = (config.max_len - len(string)) // (j_star - i_star + 1)
    # creating pump section of final_string
    pumped_string = ""
    if k > 1:
        pumped_string = "".join(string[i_star:j_star])
    final_string = "".join(string[0:i_star - 1] + pumped_string * k + string[j_star + 1:])
    return final_string


def vulnerable_tokens_present(regex):
    """
    Return true if regex has tokens with potential for exponential behavior 
    """
    for t in regex.tokens:
        if t.type == root_pb2.TokenType.QuantifierModifier or t.type == root_pb2.TokenType.GroupReference or t.type == root_pb2.TokenType.Lookaround:
            return True
    return False


def evaluate_regex(regex_protobuf: root_pb2.Expression) -> root_pb2.Output:
    """
    Run the genetic algorithm 
    """

    output = root_pb2.Output()
    evolutionary_track = []
    potential_generation = []
    regex = regex_protobuf.raw
    tokens = get_tokens(regex_protobuf)
    if testing:
        print("Tokens =", tokens)
    
    if vulnerable_tokens_present(regex_protobuf) == False:
        # skip everything 
        output.status = "No potential for vulnerability found."
        output.score = 0
        return output, [] 
    
    generation = generate_seeds(tokens)
    allowed_characters = String.printable 

    i = 0
    timed_out = False 
    start = time.time() 
    now = start 
    while (now-start) < (config.max_time*60) and timed_out == False:

        # --- MUTATE --- 
        for j in range(len(generation) - 1):
            new_mutation = single_char_mutate(generation[j], allowed_characters, 3)
            new_crossover, new_crossover_2 = crossover_mutate(generation[j], generation[j + 1])
            rand_mutation = mult_mutate(generation[j], allowed_characters) 
            potential_generation.append(new_mutation)
            potential_generation.append(new_crossover)
            potential_generation.append(new_crossover_2)
            potential_generation.append(rand_mutation)

        potential_generation = potential_generation + generation # add the old generation 
        potential_generation.append(mult_mutate(generation[-1], allowed_characters))
        potential_generation.append(single_char_mutate(generation[-1], allowed_characters, 3))

        # check for timeout 
        current_worst_string, current_worst_time = slowest_total_match_time(regex, generation)
        evolutionary_track.append(current_worst_time)
        if current_worst_time == config.timeout:
            timed_out = True 

        # print results for testing 
        if (testing and i % config.print_iter == 0):
            print("----- Generation", str(i), "-----")
            print("  ", current_worst_string)
            print("  ", current_worst_time)

        # --- PUMP --- 
        # Add this in to pump every 1000 generations 
        # Currently out because pumping takes a really long time 
        # if i % 1000 == 0 and i != 0:
        #     for input in generation:
        #         if input != '':
        #             potential_generation.append(pump(regex, input))

        # --- CULL --- 
        if timed_out == False:
            generation = cull(regex, potential_generation, config.number_of_survivors)
            potential_generation = []

        now = time.time()
        i += 1 

    # --- FINAL PUMP --- 
    worst_strings_list = []
    worst_times_list = []
    for string in generation:
        # only pump if you haven't timed out 
        if timed_out == False and len(string) < config.max_len:
            string = pump(regex, string)
        worst_strings_list.append(string)
        worst_times_list.append(match_time(regex, string))


    for i in range(len(worst_strings_list)):
        if worst_times_list[i] >= config.timeout:
            a = output.annotations.add()
            a.entity = worst_strings_list[i]
            a.note = f"This string gave the expression a run time longer than {config.timeout} second"

    if timed_out==True:
        output.status = "Vulnerability found"
        output.score = 1
    else: 
        output.status = "No vulnerability found"
        output.score = 0

    return output, evolutionary_track



"""
regex_samples = ['h.*?.*?j', '^(?=hello)[a-z]{5}', '^<\!\-\-(.*)+(\/){0,1}\-\->$'] # for testing
"""

def main():
    expr_raw = base64.b64decode(sys.argv[1])

    if not testing:
        r = root_pb2.Root()
        r.ParseFromString(expr_raw)
        output, evolution = evaluate_regex(r.expression)
        print(base64.b64encode(output.SerializeToString()).decode('utf-8'))

    else: 
        
        r = root_pb2.Expression()
        r.ParseFromString(expr_raw)
        output, evolution = evaluate_regex(r)
        print(output)

        if len(evolution) > 2:
            plt.plot(evolution)
            plt.xlabel("Generation")
            plt.ylabel("Slowest input (seconds)")
            # plt.title(expr_raw)
            plt.show()


if __name__ == "__main__":
    main()