from rolls import RollMachine
from weapons import *
from creatures import *
from manager import *

from tkinter import *


if __name__ == "__main__":

    
    
    roll = RollMachine()

    manager = ArenaManager()
    #team 1
    #manager.assignFighters(1, Hero, Shotgun, 'red')
    #manager.assignFighters(1, Hero, Pistol, 'red')
    manager.assignFighters(1, Hero(), Sword(), 'red')
    #team 2
    #manager.assignFighters(2, Human, Shotgun, "blue")
    #manager.assignFighters(1, Hero, Sword, "blue")
    manager.assignFighters(1, Human(), Sword(), 'blue')

    #winner, turns = manager.startFight()
    #print(winner, ' has won in round', turns)

    hund_fights = manager.serializeFight(10)
    proc_fights = manager.winningProcent(hund_fights)
    
    print(hund_fights)
    print(proc_fights)
