from rolls import RollMachine


class Armory():
    items = []
    def __init__(self) -> None:
        for i in [Unarmed(), Pistol(), Shotgun(), Sword()]:
            self.addItem(i)
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Armory, cls).__new__(cls)
        return cls.instance
    
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
            

    def getItems(self):
        return self.items


class Weapon():
    _type = "melee"
    _name = "name"
    _attack_mod = 0
    _damage_profile = (2, 6) #2d6
    
    #def __init__(self) -> None:
        #Armory().addItem(self)
    
    def getName(self) -> str:
        return self._name
    
    
    def getType(self) -> str:
        return self._type
    
    
    def getAttackMod(self) -> int:
        return self._attack_mod
    
    
    def getDamageProfile(self) -> tuple:
        return self._damage_profile
    
    def setName(self, name):
        self._name = name
    
    def setType(self, type):
        self._type = type
    
    def setAttackMod(self, mod):
        self._attack_mod = mod
    
    #might be better to turn it into args/kwargs function in case there is more than one kind of die to throw
    def setDamageProfile(self, dice_number, dice_value):
        self._damage_profile = (dice_number, dice_value)
    
    def doDamage(self, raises) -> int:
        _harm = 0
        
        #for weapon damage #as in setDamageProfile
        for die in range(1, self._damage_profile[0]):
            _add_harm = RollMachine().roll(self._damage_profile[1])
            _harm += _add_harm
        
        #for raises (unlimited)
        for die in range(1, raises):
            _add_harm = RollMachine().roll(6)
            _harm += _add_harm

        return _harm


class Unarmed(Weapon):
    _name = "Unarmed"
    _type = "melee"
    pass


class Pistol(Weapon):
    _name = "Pistol"
    _type = "ranged"
    _attack_mod = 0
    _damage_profile = (2, 6)


class Shotgun(Weapon):
    _name = "Shotgun"
    _type = "ranged"
    _attack_mod = 2
    _damage_profile = (3, 6)


class Sword(Weapon):
    _name = "Sword"
    _type = 'melee'
    _attack_mod = 0
    _damage_profile = (1, 8)

Unarmed()
Pistol()
Shotgun()
Sword()