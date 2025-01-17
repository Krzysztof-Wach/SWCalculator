import pytest
from main import *

class TestClass():
    
    def testRoll(self):
        RollMachine().roll(die = 6, result = 0)
        pass
    
    def testCalcRaise(self):
        assert RollMachine().calculateRises(8, 0) == 1
    
    def testDamage(self):
        assert Weapon().doDamage(1) > 0
2
