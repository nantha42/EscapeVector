import math


def norm(x):
    return math.sqrt(x[0] ** 2 + x[1] ** 2)


def add_vec(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def sub_vec(a, b):
    return [a[0] - b[0], a[1] - b[1]]


def multiply(cons, x):
    return [cons * x[0], cons * x[1]]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def angle_2vec(a, b):
    dott = dot(a,b)
    mag_a = norm(a)
    mag_b = norm(b)
    t = dott / (mag_a * mag_b)
    return math.acos(t)


def unit( x):
    n = norm(x)
    return [x[0] / n, x[1] / n]

def ret_int(x):
    return [int(x[0]),int(x[1])]
