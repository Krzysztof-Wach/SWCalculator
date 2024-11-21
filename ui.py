from rolls import RollMachine
from weapons import *
from creatures import *
from manager import *

from tkinter import *


class App():
   
    def __init__(self) -> None:
        self.master = Tk()
        self.master.title("Savage Combat Calculator")
        
        #self.teams = ['team1', 'team2']
        self.teams = {}
        self.addTeam()
        self.addTeam()
        teams_frame = self.createTeamsFrame(self.master)
        teams_frame.grid(column = 0, row = 0)
        
        self.rooster_values = {}
        
        rooster_frame = self.createRoosterFrame(self.master)
        rooster_frame.grid(row = 1)
        
        # buttons = [('Submit', 'submit')]
        # submit_button = self.createButton(self.master, buttons[0])
        # submit_button.grid(column = 0, row = 3)
        
        submit_button = self.createSubmitButton(self.master)
        submit_button.grid(column = 0, row = 2)
        
        #pack it with submit
        remove_button = self.createRemoveButton(self.master)
        remove_button.grid(column = 1, row = 2, sticky = W)
        
        quit_button = self.createQuitButton(self.master)
        quit_button.grid(column = 1, row = 3)
        
        self.master.mainloop()

    
    def createTeamsFrame(self, container):
        frame = Frame(container, name= "teams")
        
        
        for index, item in enumerate(self.teams):
            team_label = Label(frame, width= 30, text= item)
            team_field = Entry(frame, width=50 , state= DISABLED, name= str(item))
            team_label.grid(row = index, column = 0)
            team_field.grid(row = index, column = 1)
            
        return frame
    
    ### update widget
    def addTeam(self):
        #need to update frame, not yet implemented
        self.teams['team'+ str(len(self.teams)+1)] = {}
        print(self.teams)
        self.master.update()
        
    
    def removeTeam(self):
        self.teams.remove(self.teams[-1])
        self.createTeamsFrame(self.master)
        #print(self.teams)
    
    
    def createRoosterFrame(self, container):
        frame = Frame(container)
        columns = 0
        sources = {"creatures":Bestiary().getCreatures(), "weapons":Armory().getWeapons()}
        
        ###number of units added to the team
        enum_sign = Label(frame, text = 'No.')
        enum_sign.grid(row = 0, column = columns, sticky = N)
        columns +=1
        enum_field = Entry(frame, width=10) #todo enter only numbers
        enum_field.grid(row = 0, column = columns, sticky = N)
        columns +=1
        self.enum_rooster = enum_field #for setValue
        
        ###creatures, weapons
        for name, source in sources.items():
            item_frame = self.createRosterCheckbox(frame, (name, source))
            item_frame.grid(row = 0, column = columns, sticky = N)
            self.rooster_values[name] = None
            columns +=1
        
        ###teams
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
        rows = 0
        
        for index, item in enumerate(self.teams):
            rows +=1
            button = Radiobutton(frame, text = item, value = item, variable = "team", command = lambda name = "teams", item = item : self.setValue(name, item), indicatoron = 0, width = 10)
            button.grid(column = 0, row = index)
        
        blankframe = Label(frame, width= 10,)
        blankframe.grid(row = rows, column= 0)
        rows +=1
        
        ### disabled until redraw function works
        teams_button = Button(frame, text='add team', width=10,background= 'red', command=self.addTeam, state= DISABLED)
        teams_button.grid(row = rows +1 , column = 0)
        rows +=1
        
        teams_button = Button(frame, text='del team', width=10, background= 'lightgrey', command=self.removeTeam, state= DISABLED)
        teams_button.grid(row = rows +2 , column = 0)
        rows +=1

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
    
    def createRemoveButton(self, container):
        frame = Frame(container)
        
        quit_button = Button(frame, text='Remove', width=25, command = self.remove)
        quit_button.grid()
        
        return frame


    def setValue(self, variable, value):
        print(variable, value)
        self.rooster_values[variable] = value


    def submit(self):
        for value in self.rooster_values.values():
            if value is None:
                return None

        much = int(self.enum_rooster.get()) #need to not allow numbers
        
        who = self.rooster_values['creatures']
        what = self.rooster_values['weapons']
        team = self.rooster_values['teams']
        
        ### add to Entry
        self.addToTeam((much, who, what, team))
        # this_team = self.master.nametowidget("teams."+team)
        # this_team.configure(state= NORMAL)
        # this_team.insert(0, "hello")
        # this_team.configure(state= DISABLED)
    def remove(self):
        for value in self.rooster_values.values():
            if value is None:
                return None

        much = int(self.enum_rooster.get()) #need to not allow numbers
        
        who = self.rooster_values['creatures']
        what = self.rooster_values['weapons']
        team = self.rooster_values['teams']
        
        ### add to Entry
        self.removeFromTeam((much, who, what, team))
    
    def addToTeam(self, rooster): #(1, Hero, Sword, 'red')
        much, who, what, team = rooster
        current_team = self.teams[team]
        ###add rooster to team
        whowhat = (who, what)
        if whowhat in current_team:
            current_team[whowhat] = current_team[whowhat]+much
        else:
            current_team[whowhat] = much
        
        print(self.teams)
        ###update entry with new team data
        self.updateEntry(team)
    
    def removeFromTeam(self, rooster):
        much, who, what, team = rooster
        current_team = self.teams[team]
        ###add rooster to team
        whowhat = (who, what)
        if whowhat in current_team:
            current_team[whowhat] = current_team[whowhat]-much
            if current_team[whowhat] <= 0:
                
                current_team = current_team.pop(whowhat)
        else:
            return None
        
        print(self.teams)
    
    def updateEntry(self, team):
        #find entry for team
        this_team = self.master.nametowidget("teams."+team)
        
        rooster = self.teams[team]
        rooster_print = ""
        for item, value in rooster.items(): # <----- how rooster items should be passed?
            #teams{team : [(who, what, number)]}
            #merge func to see if there are changes to be made
            who, what = item
            rooster_print +=str(value) + 'x' + who.__name__ + ' '+ what.__name__ +', '
        
        this_team.configure(state= NORMAL)
        this_team.delete(0, END)
        this_team.insert(0, rooster_print)
        this_team.configure(state= DISABLED)
        #print whole rooster
        pass

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