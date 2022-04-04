# timing functions for the genetic algorithm
# Jan 2022
import re
import time
import statistics
import multiprocessing

import config 
import root_pb2



def do_match(regex, regex_input, pipe):
    time_started = time.process_time()
    regex.match(regex_input)
    time_ended = time.process_time()
    pipe.send(time_ended - time_started)


def match_time(regex, regex_input, iterations: int = 2, timeout: int = config.timeout):
    """
    Determine how long a string takes to match
    """
    times = []

    try:
        compiled_regex = re.compile(regex)
        for _ in range(iterations):
            parent_conn, child_conn = multiprocessing.Pipe()
            p = multiprocessing.Process(target=do_match, args=((compiled_regex, regex_input, child_conn, )))
            p.start()
            p.join(timeout=timeout)
            if p.is_alive():
                time_taken = timeout
                p.kill()
            else:
                time_taken = parent_conn.recv()
            times.append(time_taken)

        return statistics.mean(times)
    
    except:
        raise Exception("Could not compile regex:", regex)
        


def slowest_total_match_time(regex, generation):
    """
    Returns slowest individual in a generation based on total matching time 
    """
    slowest_time = 0
    slowest_string = ""
    for finalist in generation:
        time_taken = match_time(regex, finalist)
        if time_taken >= config.timeout:
            return finalist, config.timeout 
        elif time_taken > slowest_time:
            slowest_string = finalist
            slowest_time = time_taken
    return slowest_string, slowest_time



def slowest_individual(regex, generation):
    """
    An alternate to slowest_total_match_time
    Not currently in use
    """
    dict = {}
    ordered_generation = []
    for input in generation:
        if input != "":
            dict[input] = match_time(regex, input)
    sorted_inputs = sorted(dict.items(), key=lambda kv: kv[1])
    slowest_item = sorted_inputs[-1][0]
    slowest_time = sorted_inputs[-1][1]
    return (slowest_item, slowest_time)
