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
        
        self.rooster_values = {}
        
        rooster_frame = self.createRoosterFrame(self.master)
        rooster_frame.grid(row = 1)
        
        # buttons = [('Submit', 'submit')]
        # submit_button = self.createButton(self.master, buttons[0])
        # submit_button.grid(column = 0, row = 3)
        
        submit_button = self.createSubmitButton(self.master)
        submit_button.grid(column = 1, row = 2)
        
        quit_button = self.createQuitButton(self.master)
        quit_button.grid(column = 1, row = 3)
        
        self.master.mainloop()

    
    def createTeamsFrame(self, container):
        frame = Frame(container)
        
        
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
        columns = 0
        sources = {"creatures":Bestiary().getCreatures(), "weapons":Armory().getWeapons()}
        
        enum_field = Entry(frame, width=10)
        enum_field.grid(row = 0, column = columns, sticky = N)
        columns +=1
        self.enum_rooster = enum_field #for setValue
        
        for name, source in sources.items():
            item_frame = self.createRosterCheckbox(frame, (name, source))
            item_frame.grid(row = 0, column = columns, sticky = N)
            self.rooster_values[name] = None
            columns +=1
        
        teams_frame = self.createTeamsCheckbox(frame)
        teams_frame.grid(row = 0, column = columns, sticky = N)
        self.rooster_values['teams'] = None
        columns +=1
    
        return frame
    

    def createRosterCheckbox(self, container, checkbox_info): #checkbox_info = (name, source = list)
        frame = Frame(container)
        name, source = checkbox_info
        
        #creature_list = Radiobutton(frame)
        for index, item in enumerate(source):
            #uh oh lambda spagettioos!
            button = Radiobutton(frame, text = item.__name__, variable= name, value = item, command = lambda name = name, item = item : self.setValue(name, item), indicatoron = 0, width = 10)
            button.grid(column = 0, row = index)

        return frame

    
    def createTeamsCheckbox(self, container):
        frame = Frame(container)
        
        for index, item in enumerate(self.teams):
            button = Radiobutton(frame, text = item, value = item, variable = "team", command = lambda name = "teams", item = item : self.setValue(name, item), indicatoron = 0, width = 10)
            button.grid(column = 0, row = index)

        return frame
    

    # def createButton(self, container, button_info): #button info (name, command) 
    #     frame = Frame(container)
    #     button_name, button_command = button_info
        
    #     quit_button = Button(frame, text = button_name, width=25, command = button_command)
    #     quit_button.grid()
        
    #     return frame

    
    def createQuitButton(self, container):
        frame = Frame(container)
        
        quit_button = Button(frame, text='Quit', width=25, command=container.destroy)
        quit_button.grid()
        
        return frame


    def createSubmitButton(self, container):
        frame = Frame(container)
        
        quit_button = Button(frame, text='Submit', width=25, command = self.submit)
        quit_button.grid()
        
        return frame


    def setValue(self, variable, value):
        print(variable, value)
        self.rooster_values[variable] = value
        

    def submit(self):
        for value in self.rooster_values.values():
            print(self.rooster_values)
            if value is None:
                return None

        #much = self.enum_rooster.get()
        who = self.rooster_values['creature']
        what = self.rooster_values['weapon']
        team = self.rooster_values['teams']
        print(self.rooster_values)


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