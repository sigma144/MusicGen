import random

def generate_rhythm(beats):
    rhythm = []
    for i in range(beats * 2):
        if random.randrange(2) == 0:
            rhythm.append(i/2)