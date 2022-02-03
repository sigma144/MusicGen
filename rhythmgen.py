import random

def generate_rhythm(beats):
    rhythm = []
    for i in range(beats * 2):
        if random.randrange(5) >= 2:
            rhythm.append(i/2)
    return rhythm