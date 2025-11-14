import argparse
import itertools
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    help="Number of lines to tail",
    default=5,
    type=int,
    required=False,
)

parser.add_argument(
    "--path",
    help="File path",
    type=str
)

args = parser.parse_args()
n = args.n

def get_tail_two_pass():
    with open(args.path) as f:
        line_count = 0
        for line in f:
            line_count+=1
        # reset the cursor
        f.seek(0)
        start = line_count - n if n < line_count else 0
        tail_lines = itertools.islice(f, start, None)
        for line in tail_lines:
            print(line, end='')

def get_tail_single_pass():
    with open(args.path) as f:
        tail_lines = deque(f, maxlen=n)
        for line in tail_lines:
            print(line, end='')

get_tail_single_pass()
