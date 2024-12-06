from weapons import *
from creatures import *
from manager import *

from tkinter import *
from ui_results import *
from ui_itemCreator import *


class App():
   
    def __init__(self) -> None:
        self.master = Tk()
        self.master.title("Savage Combat Calculator")
        
        self.sources = {"creatures":Bestiary(), "weapons":Armory()}
        self.rooster_values = {}
        self.teams = {'team1' : {}, 'team2' : {}}

        #lineup view
        self.teams_frame = self.createTeamsFrame(self.master)
        self.teams_frame.grid(column = 0, row = 0)
        
        #lineup options
        self.rooster_frame = self.createRoosterFrame(self.master)
        self.rooster_frame.grid(column = 0, row = 1)
        
        #add/remove from ilneup
        self.submit_frame = self.createSubmitFrame(self.master)
        self.submit_frame.grid(column = 1, row = 1, sticky = W)
        
        ### results window
        results_window = Button(self.master, text = "FIGHT", command = self.generateResults)
        results_window.grid(column = 1, row = 0)

        self.quit_button = self.createQuitButton(self.master)
        self.quit_button.grid(column = 1, row = 2)
        
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

        for team_number in range(1, len(self.teams.keys())+1):
            team = 'team' + str(team_number)
            if team not in self.teams.keys():
                self.teams[team] = {}
                break
            else:
                team = 'team' + str(team_number+1)
                self.teams[team] = {}
        #self.createTeamsFrame(self.master)
        
        self.update()
        
    def removeTeam(self): #delete selected
        #source = self.sources['team']
        item = self.rooster_values['teams']
        if len(self.teams.keys()) != 1:
            self.teams.pop(item)
        
        self.update()


    def update(self): 
        #lineup view
        self.teams_frame = self.createTeamsFrame(self.master)
        self.teams_frame.grid(column = 0, row = 0)
        
        for team in self.teams.keys():
            self.updateTeamEntry(team)

        #lineup options
        self.rooster_frame.destroy
        self.rooster_frame = self.createRoosterFrame(self.master)
        self.rooster_frame.grid(column = 0, row = 1)

        
    def createRoosterFrame(self, container):
        frame = Frame(container, name = "rooster")
        columns = 0

        
        ###number of units added to the team
        enum_sign = Label(frame, text = 'No.')
        enum_sign.grid(row = 0, column = columns, sticky = N)
        columns +=1
        enum_field = Entry(frame, width=10) #todo enter only numbers
        enum_field.grid(row = 0, column = columns, sticky = N)
        columns +=1
        self.enum_rooster = enum_field #for setValue
        
        ###creatures, weapons
        for name, source in self.sources.items():
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
        source_list = source.getItems()

        
        #creature_list = Radiobutton(frame)
        for index, item in enumerate(source_list):
            #uh oh lambda spagettioos!
            button = Radiobutton(frame, text = item.getName(), variable= name, value = item, command = lambda name = name, item = item : self.setValue(name, item), indicatoron = 0, width = 10)
            button.grid()
        
        blankframe = Label(frame, width= 10)
        blankframe.grid()
        
        add_item = Button(frame, text='add '+ str(name), width=10,background= 'lightgrey', command= lambda name = name : self.addItem(name))
        add_item.grid()

        
        del_item = Button(frame, text='del ' + str(name), width=10, background= 'lightgrey', command= lambda name = name : self.delItem(name))
        del_item.grid()

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
        
        teams_button = Button(self.team_checkbox_frame, text='del team', width=10, background= 'lightgrey', command=self.removeTeam)
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

    
    def createQuitButton(self, container):
        frame = Frame(container)
        
        quit_button = Button(frame, text='Quit', width=25, command=container.destroy)
        quit_button.grid()
        
        return frame


    ###button commands
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
        
        self.updateTeamEntry(team)
    
    
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
        
        self.updateTeamEntry(team)
    

    def updateTeamEntry(self, team):
        #find entry for team
        this_team = self.master.nametowidget("teams."+team)
        
        rooster = self.teams[team]
        rooster_print = ""
        for item, value in rooster.items(): # <----- how rooster items should be passed?
            #teams{team : [(who, what, number)]}
            #merge func to see if there are changes to be made
            who, what = item
            rooster_print +=str(value) + 'x' + who.getName() + ' '+ what.getName() +', '
        
        this_team.configure(state= NORMAL)
        this_team.delete(0, END)
        this_team.insert(0, rooster_print)
        this_team.configure(state= DISABLED)
    

    def generateResults(self):
        valid_teams = 0
            
        for team in self.teams.values():
            if len(team) > 0:
                valid_teams+=1
        
        if valid_teams <=1:
            return None
        
        results = Results()
        results.setFight(self.teams)


    def addItem(self, kind): #creatures
        match kind:
            case "creatures":
                creator = CreatureCreator(self)
            case "weapons":
                creator = WeaponCreator(self)
        self.update()

    def delItem(self, kind):
        source = self.sources[kind]
        item = self.rooster_values[kind]
        
        source.deleteItem(item)

        self.update()
        pass


if __name__ == "__main__":

    
    
    app = App()
    
    
    #whatelsetodo
    #-fix deleting teams DONE
    #-create presets for whole teams?/configurations?
    #-get hero option in creature creator DONE
    #-check/do wounds penalty !
    #-split fight menu single || serialize
    #-make entry longer with more text
    #-streamline creators (presets/updates/)
    #-combat log