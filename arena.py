import random
from rolls import *


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


    def startFight(self, fight_name = "log.txt"):
        self.combatLog("start", fight_name)
        turn_counter = 0
        while len(self.getTeams()) > 1:
            turn_counter+=1
            self.combatLog("turn", turn_counter)
            self.takeRound()
        
        return list(self.getTeams())[0], turn_counter


    def endFight(self, winning_team):
        self.combatLog("end", winning_team)
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
                self.combatLog("state", str(fighter.getName()) +" is dead")
                self.removeUnit(fighter)
                return False
            
            
            if fighter.getActive() == False:
                self.combatLog("state", str(fighter.getName()) +" is stunned")
                return True
                
                
    def fighterRecovery(self, fighter):
            bol, result = fighter.reactivate()
            message = str(fighter.getName()) +' is recovering (' + str(result)
            
            if result < 4:
                message += ') unsuccessfully'
            else:
                if bol == False:
                    message += ') and skipping'
                else:
                    message += ') end acting immidieately'
                self.combatLog("recover", message)
                return bol
                    
                
                # bol, result = fighter.reactivate()
                
                # message = str(fighter.getName())+ " stunned, recovering roll (" + str(result)
                # if result < 4:
                #     message += "), failed"
                #     self.combatLog("stun rec", message)
                #     return False
                    
                # if bol == False:
                #     message+= '), success, skipping'
                #     self.combatLog("stun rec", message)
                #     return False
                # else:
                #     message+= '), success, acting'
                #     self.combatLog("stun rec", message)
                #     return True
                
            
            # finally:
            #     self.combatLog("state", message)

    
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
        is_alive = self.fighterState(fighter)
        if is_alive == True: #is stunned? //make different dead/stunned checks
            recover_raise = self.fighterRecovery(fighter)
            if recover_raise == False:
                return None
        elif is_alive == False:
            return None
        
        # impact = fighter.attack(weapon, target) #bool
        
        self.attack(fighter)
        
        #print('teams', self.getTeams())
        # if impact == True:
        #     self.fighterState(target)
    
    
    def attack(self, fighter):
        
        weapon = fighter.chooseWeapon()
        target = self.chooseTarget(fighter)
        
        if target == None: #if there is no target...
            return None
        
        #making attack
        strike_value = fighter.attack(weapon)
        self.combatLog("attack", (fighter, weapon, strike_value, target))
        
        match weapon.getType():
            case "melee":
                target_DC = target.getStat('parry')
            case "ranged":
                target_DC = 4
        
        #making damage
        if target_DC > strike_value:
            return None
        
        raises = RollMachine().calculateRises(strike_value - target_DC)
        damage = fighter.doDamage(weapon, raises)
        
        #taking damage
        target_toughness = target.getStat('toughness')
        
        if target_toughness > damage:
            self.combatLog("damage", (damage, "no"))
            return None
        
        wounds = target.takeDamage(damage)

        self.combatLog("damage", (damage, wounds))
        #self.fighterState(target)
    
    
    def renameFighters(self):
        
        for teams, rosters in self.getTeams().items():
            fighter_num = 0
            for fighter in rosters:
                fighter_num += 1
                weapon = fighter.chooseWeapon()
                weapon = weapon.getName()
                name = str(teams) + fighter.getName()[0:3] + str(weapon)[0:3] + str(fighter_num)
                
                fighter.setName(name)
                
                

        
        
    def combatLog(self, item, value = 0): #todo route to different class
        
        match item:
            case "start new":
                self.combat_log = open(value, "w")
            
            case "count fight":
                self.combat_log = open("log.txt", "a")
                message = "\n ==========================="
                message +="\n\t\tFIGHT " + str(value)
                message += "\n =========================="
                self.combat_log.write(message)
                
            
            case "start": #value = filename
                self.renameFighters()
                self.combat_log = open(value, "a")
                
                message = '\n'
                for team, lineup in self.getTeams().items():
                    message += str(team) + ' '
                    for fighter in lineup:
                        message += str(fighter.getName()) + ' '
                self.combat_log.write(message)
                #message = 'starting combat'
                
            case "turn": #value = turncounter
                teams = self.getTeams()
                message = "\n \n round " + str(value) + ' || '
                
                for item, value in teams.items():
                    message += str(item) + '(' + str(len(value)) + ' remaining), '
                
                self.combat_log.write(message)
            
            case "attack": #value = (fighter, weapon, strike_value, target)
                fighter, weapon, strike_value, target = value
                message = '\n \t'+ str(fighter.getName()) + ' attacking ' + str(target.getName()) + ' with ' + str(weapon.getName()) + ' (' + str(strike_value) + ')'
                self.combat_log.write(message)
            
            case "damage": #value = (damage, wounds)
                damage, wounds = value
                message = '\n \t \t' + 'dealing ' + str(damage) + ' damage, causing ' + str(wounds) + ' wounds'
                self.combat_log.write(message)
                
            case "state": #value = str
                message = '\n \t' + value
                self.combat_log.write(message)
            
            case "recover":
                message = '\n \t' + value
                self.combat_log.write(message)
            
            case "end": #value = winning team
                message = '\n' + str(value) + ' won'
                message += '\t remains: '
                for team, fighters in self.getTeams().items():
                    for fighter in fighters:
                        message += str(fighter.getName()) + ' '
                #message += 'out of ' + str(len(fighters)) get original len

                self.combat_log.write(message + '\n\n')
            
        #open/create document
        #write stuff
        #switch?
        #close doc
        #
        
        
        
        pass

if __name__ == "__main__":
    pass
    #{'team1': Human(), 'team2': Human()}
