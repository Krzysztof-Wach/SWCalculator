from creatures import *
from arena import *
import copy

class ArenaManager():
    
    #get different handlers for it
    _roster = [Humanoid, Human, Hero]
    _armory = [Unarmed, Pistol, Shotgun, Sword]
    
    
    def __init__(self) -> None:
        self._teams = {}
        
        
    def getTeams(self) -> dict:
        return self._teams
        
    
    def addTeam(self, team):
        if team not in self._teams:
            self._teams[team] = []


    def addUnit(self, unit, team):
        unit.setTeam(team)
        self._teams[team].append(unit)
    
    
    def createFighter(self, type = Human, weapon = Unarmed):

        if type in self._roster:
            fighter = type()
        else:
            print('bad fighter type')
            fighter = Human()

        if weapon in self._armory:
            fighter.addWeapon(weapon)
        else:
            print('bad weapon type')
            fighter.addWeapon(Unarmed)
        
        return fighter
    
    
    def assignFighters(self, quantity, fighters, weapons, team): #rooster
        self.addTeam(team)
        
        for unit in range(0, quantity):
            fighter = self.createFighter(fighters, weapons)
            self.addUnit(fighter, team)
    
    
    def startFight(self):
        teams = copy.deepcopy(self.getTeams()) #100% sure there is non-library way...
        arena = Arena()
        arena.setTeams(teams)
        
        #teams = self.getTeams().copy()
        winner, turns = arena.startFight()
        
        return winner, turns


    def serializeFight(self, fightsNumber):
        winnings = {}
        
        #set the book
        for team in self.getTeams():
            winnings[team] = 0
        
        for fight in range(0, fightsNumber):

            
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