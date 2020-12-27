import time
from swampy.TurtleWorld import *

welt = TurtleWorld()
tim = Turtle()
print(tim)

def quadrat(turtle, breite):
    """ zeichnet ein Quadrat mit gegebener Breite """
    if breite>0:
        for i in range(4):
            fd(turtle,int(breite))
            quadrat(turtle, breite -2)
            if breite%2 == 0:
                lt(turtle)
            else:
                rt(turtle)

fd(tim, 100)
QuadratBreite = input('wie breit soll das Quadrat werden? ')
quadrat(tim, int(QuadratBreite))
fd(tim,100)

time.sleep(3)
