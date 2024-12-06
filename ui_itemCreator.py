from tkinter import *

from weapons import *
from creatures import *




class Creator():
    parent = []
    
    def __init__(self):
        self.widgets = []
        self.master = Tk()
        self.master.title("Add")
        


class CreatureCreator(Creator):
    
    def __init__(self, master = None):
        super().__init__()
        self.master.title("Weapon")
        
        if master != None:
            self.parent.append(master)
            
        self.stats = {'spi':4, 'int':4, 'str':4, 'vig':4, 'agi':4}
        self.skills = {'fighting':4, 'shooting':4}
    
        self.preset_frame = self.createPresetFrame(self.master)
        self.preset_frame.grid(column = 0, row = 0)
    
        self.setup_frame = self.createSetupFrame(self.master)
        self.setup_frame.grid(column = 1, row = 0)
    
    
    def createSetupFrame(self, container):
        frame = Frame(container, name = 'setup')
        
        #name
        rows = 0
        name_label = Label(frame, text= "name")
        name_label.grid(column= 0, row = rows)
        name_entry = Entry(frame, name= "name")
        name_entry.grid(column = 1, row = rows)
        rows +=1
        
        #is hero? 1d6, wounds
        hero_label = Label(frame, text='Hero')
        hero_label.grid(column=0, row = rows)
        hero_checkbox = Checkbutton(frame, name = 'hero')
        hero_checkbox.grid(column = 1, row= rows, sticky= W)
        rows+=1
                
        #stats #make seperate frame?
        main_label = Label(frame, text = "Stats")
        main_label.grid(column = 0, row = rows, columnspan= 2)
        rows +=1
        statFrame = self.createStatFrame(frame)
        statFrame.grid(column = 0, row = rows, columnspan= 2)
        rows+=1
        
        main_label = Label(frame, text = "Skills")
        main_label.grid(column = 0, row = rows)
        rows+=1
        skillFrame = self.createSkillFrame(frame)
        skillFrame.grid(column = 0, row = rows)
        rows+=1
        
        #create button
        create_button = Button(frame, text = "create", command = self.getStats)
        create_button.grid(column = 0, row = rows)
        rows+=1
        
        return frame
        
    
    def createStatFrame(self, container):
        frame = Frame(container, name = "stats")
        
        #self.stats = {'spirit':4, 'int':4, 'strength':4, 'vigor':4, 'agility':4}
        
        columns = 0
        for stat, value in self.stats.items():
            stat_label = Label(frame, text = stat)
            stat_label.grid(column=columns, row= 1)
            columns+=1
            stat_entry = Entry(frame, name = stat, width = 2)
            stat_entry.grid(column = columns, row= 1)
            columns+=1
    
        return frame
    
    
    def createSkillFrame(self, container):
        frame = Frame(container, name = 'skills')
        
        #self.skills = {'fighting':4, 'shooting':4}
        rows = 0
        
        for skill, value in self.skills.items():
            skill_label = Label(frame, text = skill)
            skill_label.grid(column= 0, row= rows)
            skill_entry = Entry(frame, name = skill, width = 2)
            skill_entry.grid(column = 1, row= rows)
            rows +=1
        
        return frame
        

    def getStats(self):
        
        name = self.master.nametowidget(".setup.name").get()
        hero = self.master.nametowidget(".setup.hero").get()
        
        #self.stats = {'spirit':4, 'int':4, 'strength':4, 'vigor':4, 'agility':4}
        for stat, value in self.stats.items():
            stat_val = int(self.master.nametowidget(".setup.stats." +stat).get())
            self.stats[stat] = stat_val
        
        #self.skills = {'fighting':4, 'shooting':4}
        for skill, value in self.skills.items():
            skill_val = int(self.master.nametowidget(".setup.skills." +skill).get())
            self.skills[skill] = skill_val
        
        #which creature? is hero?
        if hero == 0:
            new_creature = Humanoid()
        elif hero == 1:
            new_creature = Hero()
        else:
            print('something wrong with hero checkup, defaulting to normal creature')
            new_creature = Humanoid()
        
        new_creature.setName(name)
            
        for stat, value in self.stats.items():
            new_creature.setStat(stat, value)
        
        for skill, value in self.skills.items():
            new_creature.setStat(skill, value)
        
        Bestiary().addItem(new_creature)
        
        self.update()
    
    
    def createPresetFrame(self, container):
        frame = Frame(container, name= "presets")
        source = Bestiary().getItems()
        rows = 0

        preset_label = Label(frame, text = "Presets")
        preset_label.grid(row = 0, column = 0, sticky = N)
        rows+=1
        
        for item in source:
            ##create radio
            button = Radiobutton(frame, text = item._name, variable= source, value = item, command = lambda item = item : self.setPreset(item), indicatoron = 0, width = 10)
            button.grid(row = rows)
            rows+=1
        
        return frame


    def update(self):
        self.preset_frame.destroy()
        self.preset_frame = self.createPresetFrame(self.master)
        self.preset_frame.grid(column = 0, row = 0)
        if len(self.parent) > 0:
            for i in self.parent:
                i.update()


    def setPreset(self, item):
        name = item.getName()
        hero = item.getHero()
        creature_stats = item.getAllStats()
        
        
        
        name_widget = self.master.nametowidget(".setup.name")
        name_widget.delete(0, END)
        name_widget.insert(0, name)
        
        hero_widget = self.master.nametowidget(".setup.hero")
        if hero == False:
            hero_widget.deselect()
        elif hero == True:
            hero_widget.select()
        
        ###transfer stats
        for item, value in creature_stats.items():
            if item in self.stats.keys():
                self.stats[item] = value
            else:
                self.skills[item] = value
        #might just split stats/skills/derivs in creatures.py later
        self.skills.pop('parry')
        self.skills.pop('toughness')
        
        self.setStats()
    
    
    def setStats(self):
        
        #widgets
        for stat, value in self.stats.items():
            stat_widget = self.master.nametowidget(".setup.stats." +stat)
            stat_widget.delete(0, END)
            stat_widget.insert(0, value)
        
        
        for skill, value in self.skills.items():
            skill_widget = self.master.nametowidget(".setup.skills." +skill)
            skill_widget.delete(0, END)
            skill_widget.insert(0, value)
    
    
class WeaponCreator(Creator):
    
    def __init__(self, master = None):
        super().__init__()
        self.master.title("Weapon")
        
        if master != None:
            self.parent.append(master)
    
        self.preset_frame = self.createPresetFrame(self.master)
        self.preset_frame.grid(column = 0, row = 0)
    
        self.setup_frame = self.createSetupFrame(self.master)
        self.setup_frame.grid(column = 1, row = 0)
        
    
    def update(self):
        self.preset_frame.destroy()
        self.preset_frame = self.createPresetFrame(self.master)
        self.preset_frame.grid(column = 0, row = 0)
        if len(self.parent) > 0:
            for i in self.parent:
                i.update()

    
    def createPresetFrame(self, container):
        frame = Frame(container, name= "presets")
        source = Armory().getItems()
        rows = 0

        preset_label = Label(frame, text = "Presets")
        preset_label.grid(row = 0, column = 0, sticky = N)
        rows+=1
        
        for item in source:
            ##create radio
            button = Radiobutton(frame, text = item._name, variable= source, value = item, command = lambda item = item : self.setPreset(item), indicatoron = 0, width = 10)
            button.grid(row = rows)
            rows+=1
        
        return frame


    def setType(self, value):
        self.weapon_type = value
        
    
    def setPreset(self, item):
        name = self.master.nametowidget(".setup.name")
        mod = self.master.nametowidget(".setup.mod")
        dice_number = self.master.nametowidget(".setup.dice_frame.dice_number")
        dice_value = self.master.nametowidget(".setup.dice_frame.dice_value")
        type_button = self.master.nametowidget(".setup." + item.getType())
        
        name.delete(0, END)
        name.insert(0, item._name)
        
        mod.delete(0, END)
        mod.insert(0, item.getAttackMod())
        
        new_dice_num, new_dice_val = item.getDamageProfile()
        dice_number.delete(0, END)
        dice_number.insert(0, new_dice_num)
        
        dice_value.delete(0, END)
        dice_value.insert(0, new_dice_val)
        
        type_button.invoke()
        
    
    def createSetupFrame(self, container):
        frame = Frame(container, name= "setup")
        rows = 0
        
        #name
        name_label = Label(frame, text= "name")
        name_label.grid(column= 0, row = rows)
        name_entry = Entry(frame, name= "name")
        name_entry.grid(column = 1, row = rows)
        rows +=1
        
        #type
        type_label = Label(frame, text= "type")
        type_label.grid(column = 0, row = rows)
        types = ["melee", "ranged"]

        
        for item in types:
            type_button = Radiobutton(frame, text= item, name = item, value= item, command= lambda item = item : self.setType(item))
            type_button.grid(column = 1, row = rows, sticky = W)
            rows +=1
        
        #attack mod
        attack_label = Label(frame, text= "att_mod")
        attack_label.grid(column= 0, row = rows)
        attack_entry = Entry(frame, name = "mod", width= 5)
        attack_entry.grid(column = 1, row = rows, sticky= W)
        rows +=1
        
        #damage ### if melee, change to make it say Si+
        damage_label = Label(frame, text= "damage")
        damage_label.grid(column= 0, row = rows)
        
        dice_frame = Frame(frame, name= 'dice_frame')
        dice_frame.grid(column= 1, row = rows, sticky= W)
        rows +=1
        
        dice_number = Entry(dice_frame, name = "dice_number", width= 5)
        dice_number.grid(column= 0, row = 0)
        
        dice_type_label = Label(dice_frame, text= "d")
        dice_type_label.grid(column= 1, row = 0)
        
        dice_value = Entry(dice_frame, name= "dice_value", width= 5)
        dice_value.grid(column= 2, row = 0)
        
        #submit
        submit_button = Button(frame, text= "submit", command = self.submitWeapon)
        submit_button.grid(column= 3, row = rows)        
        
        return frame
    
    
    def submitWeapon(self):
        ###get data
        name = self.master.nametowidget(".setup.name").get()
        type = self.weapon_type
        mod = int(self.master.nametowidget(".setup.mod").get())
        damage_number = int(self.master.nametowidget(".setup.dice_frame.dice_number").get())
        damage_value = int(self.master.nametowidget(".setup.dice_frame.dice_value").get())

        #submit data
        new_weapon = Weapon()
        new_weapon.setName(name)
        new_weapon.setType(type)
        new_weapon.setAttackMod(mod)
        new_weapon.setDamageProfile(damage_number, damage_value)
        
        Armory().addItem(new_weapon)
        
        #update previews
        self.update()
        

if __name__ == "__main__":
    # initial_creatures = [Humanoid(), Human(), Hero()]
    # initial_weapons = [Sword(), Pistol(), Shotgun()]
    
    # for item in initial_weapons:
    #     Armory().addItem(item)
    
    #creator = Creator()
    creator = CreatureCreator()
    #creator = WeaponCreator()
    creator.master.mainloop()