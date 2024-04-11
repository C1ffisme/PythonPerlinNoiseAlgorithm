import math
import random
import matplotlib.pyplot as plt
import numpy

PERLIN_SIZE = 256
SEED = 0
FREQUENCY = 0.01

def Shuffle(listarg: list):
    random.seed(SEED)
    for e in reversed(range(len(listarg))):
        index = random.randint(0,len(listarg) - 1)
        temp = listarg[e]

        listarg[e] = listarg[index]
        listarg[index] = temp

    return listarg


def MakePermutation():
    permutation = []
    for i in range(PERLIN_SIZE):
        permutation.append(i)

    Shuffle(permutation)

    for i in range(len(permutation)):
        permutation.append(permutation[i])

    return permutation


Permutation = MakePermutation()


def GetConstantVector(v):
    h = v % 4
    if h == 0:
        return tuple([1.0, 1.0])
    elif h == 1:
        return tuple([-1.0, 1.0])
    elif h == 2:
        return tuple([-1.0, -1.0])
    else:
        return tuple([1.0, -1.0])

def Fade(t):
    return ((6*t - 15)*t + 10)*t*t*t

def Lerp(t, a1, a2):
    return a1 + t*(a2-a1)


def Noise2D(x: float, y: float):
    x *= FREQUENCY
    y *= FREQUENCY

    X = int(math.floor(x) % (PERLIN_SIZE - 1))
    Y = int(math.floor(y) % (PERLIN_SIZE - 1))

    xf = x - math.floor(x)
    yf = y - math.floor(y)

    topRight = (xf - 1.0, yf - 1.0)
    topLeft = (xf, yf - 1.0)
    bottomRight = (xf - 1.0, yf)
    bottomLeft = (xf, yf)

    valueTopRight = Permutation[Permutation[X+1]+Y+1]
    valueTopLeft = Permutation[Permutation[X]+Y+1]
    valueBottomRight = Permutation[Permutation[X+1]+Y]
    valueBottomLeft = Permutation[Permutation[X]+Y]

    dotTopRight = numpy.dot(topRight, GetConstantVector(valueTopRight))
    dotTopLeft = numpy.dot(topLeft, GetConstantVector(valueTopLeft))
    dotBottomRight = numpy.dot(bottomRight, GetConstantVector(valueBottomRight))
    dotBottomLeft = numpy.dot(bottomLeft, GetConstantVector(valueBottomLeft))

    u = Fade(xf)
    v = Fade(yf)

    return Lerp(u, Lerp(v, dotBottomLeft, dotTopLeft), Lerp(v, dotBottomRight, dotTopRight))


xpix, ypix = 512, 512
pic = []
for j in range(ypix):
    pic.append([])
    for i in range(xpix):
        pic[j].append(Noise2D(i,j))

plt.imshow(pic, cmap='gray')
plt.show()
