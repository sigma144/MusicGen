import random
MAJOR = [0, 4, 7]; MINOR = [0, 3, 7]; DOMINANT = MINOR; DIMINISHED = [0, 3, 6]; SUSPENDED = [0, 5, 7]; AUGMENTED = [0, 4, 8]

CHORD_DIST_MAJOR = {
    1: 
    [(2, MINOR, 0.2), (2, MAJOR, 0.1),
        (-3, MAJOR, 0.3),
        (4, MAJOR, 1), (4, MINOR, 0.2),
        (5, MAJOR, 1), (5, MINOR, 0.1),
        (-6, MAJOR, 0.3),
        (6, MAJOR, 0.3), (6, MAJOR, 0.5),
        (-7, MAJOR, 0.3),
        (-2, MAJOR, 0.05)],

    -2: 
    [(1, MAJOR, 0.8),
        (-3, MAJOR, 0.5)],

    2: 
    [(1, MAJOR, 0.1),
        (3, MINOR, 0.1),
        (-3, MAJOR, 0.1),
        (4, MAJOR, 0.3), (4, MINOR, 0.2),
        (5, MAJOR, 1)],

    -3: 
    [(1, MAJOR, 0.3),
        (4, MAJOR, 0.5), (4, MINOR, 0.2),
        (5, MAJOR, 0.2),
        (-6, MAJOR, 0.8),
        (-7, MAJOR, 0.5),
        (-2, MAJOR, 0.2)],

    3: 
    [(2, MAJOR, 0.4),
        (6, MAJOR, 0.8)],

    4: 
    [(1, MAJOR, 0.8),
        (2, MINOR, 0.5), (2, MAJOR, 0.3),
        (3, MINOR, 0.3),
        (-3, MAJOR, 0.2),
        (4, MINOR, 0.3),
        (5, MAJOR, 1),
        (-6, MAJOR, 0.3),
        (6, MINOR, 0.5),
        (-7, MAJOR, 0.3),
        (-2, MAJOR, 0.05)],

    5: 
    [(1, MAJOR, 1),
        (2, MINOR, 0.5), (2, MAJOR, 0.3),
        (3, MINOR, 0.2),
        (-3, MAJOR, 0.5),
        (4, MINOR, 0.8),
        (-6, MAJOR, 0.3),
        (6, MINOR, 0.5),
        (-7, MAJOR, 0.2)],

    -6: 
    [(1, MAJOR, 0.7),
        (-3, MAJOR, 0.7),
        (4, MAJOR, 0.3), (4, MINOR, 0.5),
        (5, MAJOR, 0.3),
        (6, MINOR, 0.2),
        (-7, MAJOR, 0.7)],

    6: 
    [(2, MINOR, 0.2), (2, MAJOR, 0.4),
        (5, MAJOR, 0.5),
        (6, MINOR, 0.1),
        (-7, MAJOR, 0.1)],

    -7: 
    [(1, MAJOR, 0.5),
        (-3, MINOR, 0.5),
        (4, MAJOR, 0.5), (4, MINOR, 0.3),
        (5, MAJOR, 0.1), (5, MINOR, 0.3),
        (-6, MAJOR, 0.5)],
}

CHORD_DIST_MINOR = {
    2: 
    [(1, MAJOR, 0.05),
        (3, MINOR, 0.3),
        (-3, MAJOR, 0.2),
        (4, MAJOR, 0.5),
        (5, MAJOR, 0.8),
        (6, MAJOR, 0.5),
        (-7, MAJOR, 0.1),
        (-2, MAJOR, 0.05)],

    3: 
    [(1, MAJOR, 0.3),
        (2, MAJOR, 0.4), (2, MINOR, 0.5),
        (4, MAJOR, 0.5), (4, MINOR, 0.2),
        (5, MAJOR, 0.2),
        (-6, MAJOR, 0.8),
        (-7, MAJOR, 0.5),
        (-2, MAJOR, 0.2)],

    4: 
    [(1, MAJOR, 1),
        (2, DIMINISHED, 0.3),
        (-3, MAJOR, 0.2),
        (4, MAJOR, 0.1),
        (5, MAJOR, 0.3),
        (-6, MAJOR, 0.3),
        (-7, MAJOR, 0.2)],

    5: 
    [(1, MAJOR, 0.8),
        (2, MINOR, 0.1), (2, MAJOR, 0.5),
        (-3, MAJOR, 0.5),
        (4, MAJOR, 0.8), (4, MINOR, 0.5),
        (-6, MAJOR, 0.3),
        (6, MINOR, 0.1),
        (-7, MAJOR, 0.2)],

    6: 
    [(1, MAJOR, 0.5),
        (2, MINOR, 0.5), (2, MAJOR, 0.3),
        (3, MINOR, 0.5),
        (4, MAJOR, 0.5),
        (5, MAJOR, 0.3),
        (-6, MAJOR, 0.3),
        (-7, MAJOR, 0.2)],
}
    