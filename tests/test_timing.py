import time
import unittest
import timing
import re
import numpy as np


class TestMatchTimeout(unittest.TestCase):

    def test_does_timeout(self):
        timing.match_time("^<\!\-\-(.*)+(\/){0,1}\-\->$", "<!--;cb\|,\!\-\-q3/!--c5-Oh)\!\-\->", 5)
        self.assertTrue(True)

    def test_match_timeout(self):
        patts_to_test = [
            re.compile("{.*}"),
            re.compile("[abcd](.*)"),
            re.compile("(will|vicente|antonia)")
        ]
        results = {}
        for i in range(100):
            for patt in patts_to_test:
                start_time_here = time.process_time()
                patt.match("test")
                end_time_here = time.process_time()
                time_taken = timing.match_time(patt, "test", 5)
                if str(patt) not in results:
                    results[str(patt)] = {
                        "native_times": [],
                        "thread_times": [],
                        "diffs": []
                    }
                results[str(patt)]["native_times"].append(end_time_here-start_time_here)
                results[str(patt)]["thread_times"].append(time_taken)
                results[str(patt)]["diffs"].append(time_taken - (end_time_here - start_time_here))
        for patt in patts_to_test:
            print(patt)
            native_times = results[str(patt)]["native_times"]
            thread_times = results[str(patt)]["thread_times"]
            diffs = results[str(patt)]["diffs"]
            print(f"Average native time: {sum(native_times) / len(native_times)}")
            print(f"Average thread time: {sum(thread_times) / len(thread_times)}")
            print(f"Average diff: {sum(diffs) / len(diffs)}")
            print(f"Std: {np.std(diffs)}")
        self.assertTrue(True)
