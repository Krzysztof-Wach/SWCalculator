from weapons import *



class Bestiary():
    
    items = []
    
    def __init__(self) -> None:
        
        for i in [Humanoid(), Human(), Hero()]:
            self.addItem(i)
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Bestiary, cls).__new__(cls)
        return cls.instance
    
    def getItems(self):
        return self.items
    
    def addItem(self, item):
        items_names = []
        
        for i in self.items:
            items_names.append(i.getName())
        if item.getName() not in items_names:
            self.items.append(item)

    
    def deleteItem(self, item):
        for i in self.items:
            if i.getName() == item.getName():
                self.items.remove(i)
                break

class Creature():

    def __init__(self):
        # bestiariusz.append[self.__class__]
        #Bestiary().addItem(self.__class__)
        self._name = "Creature"
        self.hero = False
        self._health = 1
        self._max_health = self._health
        self._stats = {'spi':4, 'int':4, 'str':4, 'vig':4, 'agi':4}
        self._team = None
        self.deriveStats()

    def getName(self):
        return self._name

    def getStat(self, stat):
        return self._stats[stat]
    
    def getHealth(self) -> int:
        return self._health
    
    def getMaxHealth(self) -> int:
        return self._max_health
    
    
    def getAllStats(self):
        return self._stats
    
    
    def getTeam(self):
        return self._team

    def getHero(self):
        return self.hero
    
    def setStat(self, stat, new_value):
        self._stats[stat] = new_value
        if stat == "fighting" or stat == "vig":
            self.deriveStats()
    
    def setHealth(self, health):
        self._health = int(health)
        
        if health <= 0:
            self.setAlive(False)
    
    def setMaxHealth(self, health) :
        self._max_health = health


    def setTeam(self, team):
        self._team = team


    def deriveStats(self): # set parry and toughness
        
        if 'fighting' in self._stats:
            self._stats["parry"] = int(self._stats['fighting']/2 +2)
        else:
            self._stats["parry"] = 2
        
        self._stats["toughness"] = int(self._stats['vig']/2 +2)


    def testStat(self, stat):
        wound_mod = self.getMaxHealth() - self.getHealth()
        if wound_mod > 3:
            wound_mod = 3
        
        if stat in self._stats:
            result = RollMachine().roll(self.getStat(stat))
        else:
            print("improvisation roll")
            result = RollMachine().roll(4) - 2
            
            
        result = result - wound_mod

        return result


class Humanoid(Creature):
    

    def __init__(self):
        super().__init__()
        
        self._name = "Humanoid"
        
        
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

    def getName(self):
        return self._name

    
    def getWeapons(self) -> list:
        return self._weapons
    
    
    def getActive(self) -> bool:
        return self._isActive
    
    
    def getAlive(self) -> bool:
        return self._isAlive
    
    
    def getWeapons(self):
        return self._weapons
    
    
    def setName(self, name):
        self._name = name


    def addWeapon(self, weapon):
        if weapon not in self._weapons and isinstance(weapon, Weapon):
            self._weapons.append(weapon)


    def setActive(self, state):
        self._isActive = state


    def setAlive(self, state):
        self._isAlive = state


    def attack(self, weapon): #return if the attack caused wounds
        weapon_type = weapon.getType()
        damage = 0
        
        if weapon_type == 'melee': #switch
            strike_value = self.meleeAttack(weapon)
            #target_defence = target.getStat("parry")
        elif weapon_type == 'ranged':
            strike_value = self.rangedAttack(weapon)
            #target_defence = 4
        #else, improvise?
        
        #maybe should delegate target.takedamage() to the arena?
        # if strike_value > target_defence:
        #     damage = self.doDamage( strike_value, target_defence, weapon)
        #     target.takeDamage(damage)
        #     return True
        # else:
        #     return False
        return strike_value
        
    
    
    def meleeAttack(self, weapon):
        weapon_att_mod = weapon.getAttackMod()
        
        strike_value = self.testStat('fighting') + weapon_att_mod
        
        return strike_value

    
    def rangedAttack(self, weapon):
        weapon_att_mod = weapon.getAttackMod()
        
        strike_value = self.testStat('shooting') + weapon_att_mod
        
        return strike_value


    def doDamage(self, weapon, raises) -> int: #def doDamage(self, strike_value, targets_defence, weapon) -> int:
        weapon_type = weapon.getType()
        
        # raises = RollMachine().calculateRises(strike_value, targets_defence)
        damage = weapon.doDamage(raises)
        
        if weapon_type == "melee":
                damage += RollMachine().roll(self.getStat("str"))
            
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
        
        result = self.testStat('spi')
        raises = RollMachine().calculateRises(result, 4)
        
        if result >= 4:
            self.setActive(True)
        
        if raises > 0:
            return (True, result)
        else:
            return (False, result)


class Human(Humanoid):
    #_stats = {'spi':6, 'int':6, 'str:6, 'vig':6, 'agi':6}
    
    
    def __init__(self):
        super().__init__()

        self._name = "Human"

        for stat in self._stats:
            self.setStat(stat, 6) 

        #add stats
        _skills = {'fighting': 2, 'shooting':6}
        for key in _skills:
            self.setStat(key, _skills[key])


class Hero(Humanoid):
    
    
    def __init__(self):
        super().__init__()
        
        self._name = "Hero"
        self.hero = True
        
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
        

