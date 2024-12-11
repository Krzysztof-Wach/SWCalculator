from creatures import *
from arena import *
import copy

class ArenaManager():
    
    #get different handlers for it
    
    
    def __init__(self) -> None:
        self._teams = {}
        
        self._roster = Bestiary().getItems()
        self._armory = Armory().getItems()
        
        
        
    def getTeams(self) -> dict:
        return self._teams
        
    
    def addTeam(self, team):
        if team not in self._teams:
            self._teams[team] = []


    def addUnit(self, unit, team):
        unit.setTeam(team)
        self._teams[team].append(unit)
    
    
    def createFighter(self, creature, weapon):
        self._roster = Bestiary().getItems()
        self._armory = Armory().getItems()
        
        #validation. make seperate?
        creature_names = []
        weapon_names = []
        for item in self._roster:
            creature_names.append(item.getName())
        for item in self._armory:
            weapon_names.append(item.getName())
        
        if creature.getName() in creature_names:
            fighter = copy.deepcopy(creature)
            
        else:
            print('bad fighter')
        
        if weapon.getName() in weapon_names:
            fighter.addWeapon(weapon)
        else:
            print('bad weapon')
        
        return fighter
    
    
    def assignFighters(self, quantity, fighters, weapons, team): #rooster
        self.addTeam(team)
        
        for unit in range(0, quantity):
            fighter = self.createFighter(fighters, weapons)
            self.addUnit(fighter, team)
    
    
    def startFight(self):
        teams = copy.deepcopy(self.getTeams()) #100% sure there is non-library way...
        arena = Arena()
        arena.combatLog("fight", "log.txt")
        arena.setTeams(teams)
        winner, turns = arena.startFight()
        
        return winner, turns


    def serializeFight(self, fightsNumber):
        winnings = {}
        
        Arena().combatLog("start new", "log.txt")
        
        #set the book
        for team in self.getTeams():
            winnings[team] = 0
        
        for fight in range(0, fightsNumber):
            Arena().combatLog("count fight", fight+1)
            winner, turns = self.startFight()
            winnings[winner] += 1
        
        return winnings
    
    
    def winningProcent(self, teamWins):
        winnings = {}
        #{team: num_won,}
        num_rounds = 0
        for team, wins in teamWins.items():
            num_rounds += wins
        
        for team, wins in teamWins.items():
            winnings[team] = str((wins/num_rounds)*100) + '%'
        
        return winnings


if __name__ == "__main__":
    roll = RollMachine()

    manager = ArenaManager()
    #quantity, fighters, weapon, team
    manager.assignFighters(1, Hero(), Sword(), 'red')

    manager.assignFighters(1, Human(), Sword(), 'blue')

    hund_fights = manager.serializeFight(10)
    proc_fights = manager.winningProcent(hund_fights)
    
    print(hund_fights)
    print(proc_fights)
