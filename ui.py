from rolls import RollMachine
from weapons import *
from creatures import *
from manager import *

from tkinter import *


class App():
    
    def __init__(self) -> None:
        self.master = Tk()
        self.master.title("Savage Combat Calculator")
        
        self.teams = ['Team1', 'Team2']
        teams_frame = self.createTeamsFrame(self.master)
        teams_frame.grid(column = 0, row = 0)
        
        rooster_frame = self.createRoosterFrame(self.master)
        rooster_frame.grid(row = 1)
        
        
        quit_button = self.createQuitButton(self.master)
        quit_button.grid(column = 1, row = 3)
        
        self.master.mainloop()

    
    def createTeamsFrame(self, container):
        frame = Frame(container)
        
        #two default teams
        
        
        for index, item in enumerate(self.teams):
            team_label = Label(frame, width= 30, text= item)
            team_field = Entry(frame, width=50 , state= DISABLED)
            team_label.grid(row = index, column = 0)
            team_field.grid(row = index, column = 1)
            
        return frame
    
    
    def addTeam(self):
        
        #need to update frame, not yet implemented
        self.teams.append('team' + str(len(self.teams)))
        self.createTeamsFrame(self.master)
    
    
    def createRoosterFrame(self, container):
        frame = Frame(container)
        
        creature_frame = self.createCreatureCheckbox(frame)
        creature_frame.grid(row = 0, column = 0, sticky = N)
        
        weapon_frame = self.createWeaponCheckbox(frame)
        weapon_frame.grid(row = 0, column = 1, sticky = N)
        
        teams_frame = self.createTeamsCheckbox(frame)
        teams_frame.grid(row = 0, column = 2, sticky = N)
    
        return frame
    
    
    def createCreatureCheckbox(self, container):
        frame = Frame(container)
        
        #creature_list = Radiobutton(frame)
        for index, item in enumerate(Bestiary().getCreatures()):
            button = Radiobutton(frame, text = item.__name__, value = item, variable= 'creature' , indicatoron = 0, width = 10)
            button.grid(column = 0, row = index)
            #creature_list.insert(index, item)

        return frame

    
    def createWeaponCheckbox(self, container):
        frame = Frame(container)
        
        #creature_list = Radiobutton(frame)
        for index, item in enumerate(Armory().getWeapons()):
            button = Radiobutton(frame, text = item.__name__, value = item, variable= 'weapon' , indicatoron = 0, width = 10)
            button.grid(column = 0, row = index)
            #creature_list.insert(index, item)
        
        return frame

    
    def createTeamsCheckbox(self, container):
        frame = Frame(container)
        
        for index, item in enumerate(self.teams):
            button = Radiobutton(frame, text = item, value = item, variable = "team", indicatoron = 0, width = 10)
            button.grid(column = 0, row = index)

        return frame
    
    
    def createQuitButton(self, container):
        frame = Frame(container)
        
        quit_button = Button(frame, text='Quit', width=25, command=container.destroy)
        quit_button.grid()
        
        return frame


    def createQuitButton(self, container):
        frame = Frame(container)
        
        quit_button = Button(frame, text='Quit', width=25, command=container.destroy)
        quit_button.grid()
        
        return frame


if __name__ == "__main__":
    
    
    initial_creatures = [Humanoid(), Human(), Hero()]
    initial_weapons = [Sword(), Pistol(), Shotgun()]
    
    app = App()
    
    


    # #root = Tk()
    # #app = App(root)
    # #root.mainloop()


    # master = Tk()
    # master.title('Savage Combat Calculator')
    
    
    # #Label(master, text='team1').grid(row=0)
    # #Label(master, text='team2').grid(row=1)
    # teams_frame = Frame(master)
    # team1 = Entry(teams_frame, width=100)
    # team2 = Entry(teams_frame, width=100)
    # #team1.grid(row = 0, column = 1)
    # #team2.grid(row = 1, column = 1)
    # #team1.pack()
    # #team2.pack()
    
    # teams_frame.pack()
    
    
    # beast_list = Listbox(master)
    
    # for index, item in enumerate(Bestiary().getCreatures()):
    #     beast_list.insert(index, item)
    # #beast_list.pack()
    
        
    # print(Bestiary().getCreatures())


    
    
    # #Button(master, text='Quit', width=25, command=master.destroy).grid(row=3)
    # quit = Button(master, text='Quit', width=25, command=master.destroy)
    # quit.pack()
    # mainloop()