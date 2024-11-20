from rolls import RollMachine


class Armory():
    
    weapons = []
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Armory, cls).__new__(cls)
        return cls.instance
    
    def addWeapon(self, creature):
        if creature not in self.weapons:
            self.weapons.append(creature)

    def getWeapons(self):
        return self.weapons



class Weapon():
    _type = "melee"
    _attack_mod = 0
    _damage_profile = (2, 6) #2d6
    
    def __init__(self) -> None:
        Armory().addWeapon(self.__class__)
    
    
    def getType(self) -> str:
        return self._type
    
    
    def getAttackMod(self) -> int:
        return self._attack_mod
    
    
    def getDamageProfile(self) -> tuple:
        return self._damage_profile
    
    
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
    _type = "melee"
    pass


class Pistol(Weapon):
    _type = "ranged"
    _attack_mod = 0
    _damage_profile = (2, 6)


class Shotgun(Weapon):
    _type = "ranged"
    _attack_mod = 2
    _damage_profile = (3, 6)


class Sword(Weapon):
    _type = 'melee'
    _attack_mod = 0
    _damage_profile = (1, 8)

