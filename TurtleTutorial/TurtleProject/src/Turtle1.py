import time
from swampy.TurtleWorld import *

welt = TurtleWorld()
tim = Turtle()
print(tim)

fd(tim, 100)
lt(tim)

QuadratBreite = input('wie breit solldas Quadrat werden?')

fd(tim,int(QuadratBreite))

time.sleep(5)
