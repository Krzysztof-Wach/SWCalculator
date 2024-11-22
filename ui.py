from rolls import RollMachine
from weapons import *
from creatures import *
from manager import *

from tkinter import *


class App():
   
    def __init__(self) -> None:
        self.master = Tk()
        self.master.title("Savage Combat Calculator")
        
        self.rooster_values = {}
        #self.teams = ['team1', 'team2']
        self.teams = {}

        #lineup view
        self.teams_frame = self.createTeamsFrame(self.master)
        self.teams_frame.grid(column = 0, row = 0)
        
        #lineup options
        self.rooster_frame = self.createRoosterFrame(self.master)
        self.rooster_frame.grid(column = 0, row = 1)
        
        #add/remove from ilneup
        self.submit_frame = self.createSubmitFrame(self.master)
        self.submit_frame.grid(column = 1, row = 1, sticky = W)
        # buttons = [('Submit', 'submit')]
        # submit_button = self.createButton(self.master, buttons[0])
        # submit_button.grid(column = 0, row = 3)

        #quit app
        self.quit_button = self.createQuitButton(self.master)
        self.quit_button.grid(column = 2, row = 2)
        
        self.addTeam()
        self.addTeam()
        
        self.master.mainloop()


    ###TO DO make Label expand and rooster items wrapup if needed
    def createTeamsFrame(self, container):
        frame = Frame(container, name= "teams")
        
        for index, item in enumerate(self.teams):
            team_label = Label(frame, width= 30, text= item)
            team_field = Entry(frame, width=50 , state= DISABLED, name= str(item))
            team_label.grid(row = index, column = 0)
            team_field.grid(row = index, column = 1)
        
        frame.update()
            
        return frame
    
    
    def addTeam(self):
        #need to update frame, not yet implemented
        new_team = 'team'+ str(len(self.teams)+1)
        self.teams[new_team] = {}
        print(self.teams)
        
        #self.createTeamsFrame(self.master)
        #self.createRoosterFrame(self.master)
        self.createTeamsFrame(self.master)
        
        # button = Radiobutton(self.team_checkbox_frame, text = new_team, value = new_team, variable = "team", command = lambda name = "teams", item = new_team : self.setValue(name, item), indicatoron = 0, width = 10)
        # button.grid(column = 0)
        
        ### teams entry fields
        # self.teams_frame = self.createTeamsFrame(self.master)
        # self.teams_frame.grid(column = 0)
        # ### teams checkbox
        # self.rooster_frame = self.createRoosterFrame(self.master)
        # self.rooster_frame.grid(column = 0)
        #self.master.update()
        self.update()
        
        
    def update(self):
        #lineup view
        self.teams_frame.destroy
        self.teams_frame = self.createTeamsFrame(self.master)
        self.teams_frame.grid(column = 0, row = 0)
        
        #lineup options
        self.rooster_frame.destroy
        self.rooster_frame = self.createRoosterFrame(self.master)
        self.rooster_frame.grid(column = 0, row = 1)
        
        #add/remove from ilneup
        self.submit_frame.destroy
        self.submit_frame = self.createSubmitFrame(self.master)
        self.submit_frame.grid(column = 1, row = 1, sticky = W)
        # buttons = [('Submit', 'submit')]
        # submit_button = self.createButton(self.master, buttons[0])
        # submit_button.grid(column = 0, row = 3)

        #quit app
        self.quit_button.destroy
        self.quit_button = self.createQuitButton(self.master)
        self.quit_button.grid(column = 2, row = 2)
        
    
    def removeTeam(self):
        self.teams.remove(self.teams[-1])
        self.createTeamsFrame(self.master)
        #print(self.teams)
    
    
    def createRoosterFrame(self, container):
        frame = Frame(container, name = "rooster")
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
            #self.rooster_values[name] = None  ###not really necessary???
            columns +=1
        
        ###teams
        teams_frame = self.createTeamsCheckbox(frame)
        teams_frame.grid(row = 0, column = columns, sticky = N)
        #self.rooster_values['teams'] = None ###not really necessary???
        columns +=1

        frame.update()
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
        self.team_checkbox_frame = Frame(container, name = "box")
        rows = 0
        
        for index, item in enumerate(self.teams):
            rows +=1
            button = Radiobutton(self.team_checkbox_frame, text = item, value = item, variable = "team", command = lambda name = "teams", item = item : self.setValue(name, item), indicatoron = 0, width = 10)
            button.grid(column = 0)
            
        blankframe = Label(self.team_checkbox_frame, width= 10)
        blankframe.grid(row = rows, column= 0)
        rows +=1
        
        ### disabled until redraw function works
        teams_button = Button(self.team_checkbox_frame, text='add team', width=10,background= 'lightgrey', command=self.addTeam)
        teams_button.grid()
        rows +=1
        
        teams_button = Button(self.team_checkbox_frame, text='del team', width=10, background= 'lightgrey', command=self.removeTeam, state= DISABLED)
        teams_button.grid()
        rows +=1

        return self.team_checkbox_frame
    
    
    def createSubmitFrame(self, container):
        frame = Frame(container)
        
        submit_button = Button(frame, text='Submit', width=15, command = self.submit)
        submit_button.grid(column = 0, row = 0)
        
        #pack it with submit
        remove_button = Button(frame, text='Remove', width=15, command = self.remove)
        remove_button.grid(column = 0, row = 2)
        
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


    def setValue(self, variable, value):
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
        
        self.updateEntry(team)
    

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