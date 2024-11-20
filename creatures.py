from weapons import *



class Bestiary():
    
    creatures = []
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Bestiary, cls).__new__(cls)
        return cls.instance
    
    def addCreature(self, creature):
        if creature not in self.creatures:
            self.creatures.append(creature)

    def getCreatures(self):
        return self.creatures

class Creature():


    def __init__(self):
        # bestiariusz.append[self.__class__]
        Bestiary().addCreature(self.__class__)
        self.name = "Creature"
        self._stats = {'spirit':4, 'int':4, 'strength':4, 'vigor':4, 'agility':4}
        self._team = None
        self.deriveStats()


    def getStat(self, stat):
        return self._stats[stat]    
    
    
    def getAllStats(self):
        return self._stats
    
    
    def getTeam(self):
        return self._team
    
    
    def setStat(self, stat, new_value):
        self._stats[stat] = new_value
        if stat == "fighting" or stat == "vigor":
            self.deriveStats()


    def setTeam(self, team):
        self._team = team


    def deriveStats(self): # set parry and toughness
        
        if 'fighting' in self._stats:
            self._stats["parry"] = int(self._stats['fighting']/2 +2)
        else:
            self._stats["parry"] = 2
        
        self._stats["toughness"] = int(self._stats['vigor']/2 +2)


    def testStat(self, stat):
        if stat in self._stats:
            result = RollMachine().roll(self.getStat(stat))
        else:
            print("improvisation roll")
            result = RollMachine().roll(4) - 2

        return result


class Humanoid(Creature):
    

    def __init__(self):
        super().__init__()
        
        self.name = "Humanoid"
        
        self._health = 1
        self._weapons = []
        self._isAlive = True
        self._isActive = True
        
        #every humanoid can attack as unarmed
        unarmed = Unarmed()
        self.addWeapon(unarmed)
        
        #add stats
        _skills = {'fighting': 4, 'shooting':4}
        for key in _skills:
            self.setStat(key, _skills[key])
            
        self.deriveStats()


    def getHealth(self) -> int:
        return self._health
    
    
    def getWeapons(self) -> list:
        return self._weapons
    
    
    def getActive(self) -> bool:
        return self._isActive
    
    
    def getAlive(self) -> bool:
        return self._isAlive
    
    
    def setHealth(self, health):
        self._health = int(health)
        
        if health <= 0:
            self.setAlive(False)


    def addWeapon(self, weapon):
        if weapon not in self._weapons and isinstance(weapon, Weapon):
            self._weapons.append(weapon)


    def setActive(self, state):
        self._isActive = state


    def setAlive(self, state):
        self._isAlive = state


    def attack(self, weapon, target) -> bool: #return if the attack caused wounds
        weapon_type = weapon.getType()
        damage = 0
        
        if weapon_type == 'melee':
            strike_value = self.meleeAttack(weapon)
            target_defence = target.getStat("parry")
        elif weapon_type == 'ranged':
            strike_value = self.rangedAttack(weapon)
            target_defence = 4
        #else, improvise?
        
        #maybe should delegate target.takedamage() to the arena?
        if strike_value > target_defence:
            damage = self.doDamage( strike_value, target_defence, weapon)
            target.takeDamage(damage)
            return True
        else:
            return False
        
    
    
    def meleeAttack(self, weapon):
        weapon_att_mod = weapon.getAttackMod()
        
        strike_value = self.testStat('fighting') + weapon_att_mod
        
        return strike_value

    
    def rangedAttack(self, weapon):
        weapon_att_mod = weapon.getAttackMod()
        
        strike_value = self.testStat('shooting') + weapon_att_mod
        
        return strike_value


    def doDamage(self, strike_value, targets_defence, weapon) -> int:
        weapon_type = weapon.getType()
        
        raises = RollMachine().calculateRises(strike_value, targets_defence)
        damage = weapon.doDamage(raises)
        
        if weapon_type == "melee":
                damage += RollMachine().roll(self.getStat("strength"))
            
        return damage

    
    def takeDamage(self, damage) -> int:
        defence = self.getStat('toughness')
        
        if damage >= defence:
            new_wounds = RollMachine().calculateRises(damage, defence)
            
            if self.getActive() == True:
                self._isActive = False
            else:
                new_wounds+=1
            
            
            health = self.getHealth()
            health -= new_wounds
            self.setHealth(health)
        
            return new_wounds
        else:
            return 0

    #choosing lates added weapon
    def chooseWeapon(self):
        return self._weapons[-1]
    
    
    def reactivate(self):
        
        result = self.testStat('spirit')
        raises = RollMachine().calculateRises(result, 4)
        
        if result >= 4:
            self.setActive(True)
        
        if raises > 0:
            return True
        else:
            return False


class Human(Humanoid):
    #_stats = {'spirit':6, 'int':6, 'strength':6, 'vigor':6, 'agility':6}
    
    
    def __init__(self):
        super().__init__()

        self.name = "Human"

        for stat in self._stats:
            self.setStat(stat, 6) 

        #add stats
        _skills = {'fighting': 6, 'shooting':6}
        for key in _skills:
            self.setStat(key, _skills[key])


class Hero(Humanoid):
    
    
    def __init__(self):
        super().__init__()
        
        self.name = "Hero"
        
        self.setHealth(3)
        
        for stat in self._stats:
            self.setStat(stat, 6)


    def testStat(self, stat):
        result = super().testStat(stat)
        
        wild_result = RollMachine().roll(6)
        
        if result > wild_result:
            return result
        else:
            return wild_result
        

