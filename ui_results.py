from tkinter import *

from manager import *

class Results():
    
    
    def __init__(self) -> None:
        self.master = Tk()
        self.master.title("Combat Results")
        
        self.manager = ArenaManager()
        
        self.results_frame = self.createResultsFrame(self.master)
        self.results_frame.grid(column= 0, row = 0)
        
        self.serialize_frame = self.createSerializeFrame(self.master)
        self.serialize_frame.grid(column = 1, row = 0)
    
    
    def setFight(self, teams):
        
        for team, rooster in teams.items():
            self.manager.addTeam(team)
            
            for fighter, number in rooster.items():
                who, what = fighter
                #who = copy.deepcopy(who)
                self.manager.assignFighters(number, who, what, team)
    
    
    def createResultsFrame(self, container):
        frame = Frame(container, name= "results")
        
        start_fight_button = Button(frame, text = 'start fight', command = self.startFight)
        start_fight_button.grid(column = 0, row = 0, sticky= W)
        
        results_entry = Entry(frame, state= DISABLED, name= 'result')
        results_entry.grid(column = 0, row = 1)
        
        return frame


    def startFight(self):
        result = self.manager.startFight()
        self.setResult(result)


    def setResult(self, result):
        result_entry = self.master.nametowidget(".results.result")
        team, turn = result
        result_text = str(team) + " won in turn " + str(turn)
        
        result_entry.configure(state= NORMAL)
        result_entry.delete(0, END)
        result_entry.insert(0, result_text)
        result_entry.configure(state= DISABLED)
        
    
    def createSerializeFrame(self, container):
        frame = Frame(container, name = "serializer")
        
        #entry (how many fights, def 100)
        frame_name = Label(frame, text= "serialize fight", width= 30)
        frame_name.grid(column = 0, row = 0, sticky= N, columnspan= 2)
        
        no_fights_label = Label(frame, text = "No.", width= 5)
        no_fights_label.grid(column = 0, row = 1, sticky = E)
        no_fights = Entry(frame, width= 5, name= 'number_fights')
        no_fights.insert(0, "100") 
        no_fights.grid(column = 1, row = 1, sticky= W)

        #start        
        start_fight_button = Button(frame, text = 'serialize fights', command = self.serializeFight)
        start_fight_button.grid(column = 0, row = 3, sticky= E)
        
        results_entry = Entry(frame, state= DISABLED, name= 'result', width= 30)
        results_entry.grid(column = 0, row = 4, columnspan= 2)
        #print results
    
        return frame
    
    
    def serializeFight(self):
        fights = self.master.nametowidget(".serializer.number_fights").get()
        fights = int(fights)
        
        result = self.manager.serializeFight(fights)
        #print(result)
        self.setSerialization(result)
        
        
    def setSerialization(self, result): #{team1: #wins, ...}
        result_entry = self.master.nametowidget(".serializer.result")
        #result_text = str(team) + " won in turn " + str(turn)
        
        result_entry.configure(state= NORMAL)
        result_entry.delete(0, END)
        result_entry.insert(0, result)
        result_entry.configure(state= DISABLED)
        

if __name__ == "__main__":
    teams = {'team1': {(Humanoid(), Sword()): 1}, 'team2': {(Humanoid(), Sword()): 1}}
    results = Results()
    results.setFight(teams)
    results.master.mainloop()
    