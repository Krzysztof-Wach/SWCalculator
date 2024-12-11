import random
import math

class RollMachine():

    ### make rolls (d6)
    def roll(self, die, result = 0):
        _result = random.randint(1, die)
        _res_sum = result + _result
        
        ### make rolls explode
        if _result == die and _res_sum < 40: ### make a roll buffer
            _res_exp = RollMachine.roll(die, _res_sum)
            _res_sum+=_res_exp
        
        return _res_sum


    #raises are dices buissness, right?
    def calculateRises(self, result, difficulty = 0) -> int:
        
        raises = math.floor( (result - difficulty) /4)
        if raises < 0:
            raises = 0
        
        return raises
    

if __name__ == "__main__":
    print(RollMachine().roll(20))