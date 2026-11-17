from random import randint, random

def create_random_float(lower: int, upper: int):
    int_portion = randint((lower+1), (upper-1))
    rv = int_portion + random()
    return rv

def create_random_lat():
    return create_random_float(lower=-90, upper=90)

def create_random_lon():
    return create_random_float(lower=-180, upper=180)