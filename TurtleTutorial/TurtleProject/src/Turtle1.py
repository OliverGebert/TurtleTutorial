import time
from swampy.TurtleWorld import *

welt = TurtleWorld()
tim = Turtle()
print(tim)

def fakultaet(n):
    space = ' ' * n
    print(space, 'Fakultät: ', n)
    if n < 0:
        print("Fakultät kann nur von positiven ganzen Zahlen berechnet werden")
        return None
    elif n == 0:
        return 1
    else:
        return n*fakultaet(n-1)

def quadrat(turtle, breite):
    """ zeichnet ein Quadrat mit gegebener Breite """
    if breite > 0:
        for i in range(4):
            fd(turtle,int(breite))
            quadrat(turtle, breite -5)
            if breite%2 == 0:
                lt(turtle)
            else:
                rt(turtle)

fd(tim, 100)
QuadratBreite = input('wie breit soll das Quadrat werden? ')
print(fakultaet(int(QuadratBreite)))
quadrat(tim, int(QuadratBreite))
fd(tim,100)

time.sleep(5)
