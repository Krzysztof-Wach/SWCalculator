import random


class Arena():
    
    
    def __init__(self) -> None:
        self._teams = {}
        

    def getTeams(self) -> dict:
        return self._teams
    
    
    def setTeams(self, teams):
        self._teams = teams


    def removeTeam(self, team):
        self._teams.pop(team)
        #check if there are any teams left
        if len(self.getTeams()) == 1:
            remaining_team = list(self.getTeams())[0]
            self.endFight(remaining_team)


    def removeUnit(self, defeted_fighter):
        teams = self.getTeams().copy()
        
        for team_name, team in teams.items():
            for fighter in team:
                if fighter is defeted_fighter:
                    self._teams[team_name].remove(defeted_fighter)

            if len(team) == 0:
                self.removeTeam(team_name)


    def startFight(self):
        turn_counter = 0
        while len(self.getTeams()) > 1:
            turn_counter+=1
            self.takeRound()
        
        return list(self.getTeams())[0], turn_counter


    def endFight(self, winning_team):
        return winning_team


    def makeTurnOrder(self):
        turn_order = []
        teams = self.getTeams()
        
        for team in teams:
            for fighter in teams[team]:
                turn_order.append(fighter)
                
        random.shuffle(turn_order)
        return turn_order


    def fighterState(self, fighter):
            if fighter.getAlive() == False:
                self.removeUnit(fighter)
                return False
            if fighter.getActive() == False:
                if fighter.reactivate() == False:
                    return False
                else:
                    return True
    
    
    def chooseTarget(self, fighter):
        fighter_team = fighter.getTeam()
        
        different_teams = self.getTeams().copy()
        different_teams.pop(fighter_team)
        different_teams = list(different_teams.values())
        
        if len(different_teams) == 0:
            return None
        
        defender_team = random.choice(different_teams)
        defender = random.choice(defender_team)
        
        return defender
    
    
    def takeRound(self):
        turn_order = self.makeTurnOrder()
        
        ###make a function for it
        for fighter in turn_order:
            self.takeTurn(fighter)
            
    
                
    def takeTurn(self, fighter):
        if self.fighterState(fighter) == False: #can this fighter act?
            return None

        weapon = fighter.chooseWeapon()
        target = self.chooseTarget(fighter)

        if target == None: #if there is no target...
            return None
        
        impact = fighter.attack(weapon, target) #bool
        
        #print('teams', self.getTeams())
        if impact == True:
            self.fighterState(target)

if __name__ == "__main__":
    pass
    #{'team1': Human(), 'team2': Human()}
