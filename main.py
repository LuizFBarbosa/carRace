from controleF import Controle
import threading
from game import CarRacing

controle = Controle()
game = CarRacing()

t1 = threading.Thread(target = controle.start)
t2 = threading.Thread(target = game.main)

t1.start()
t2.start()

t1.join()
t2.join()