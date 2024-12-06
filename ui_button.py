from tkinter import *


class App():
    
    def __init__(self) -> None:
        self.master = Tk()
        
        self.buttons_list = ['b1', 'b2']
        buttons = self.createButton(self.master)
        buttons.grid(column= 0, row = 0)
        
        add_button = Button(self.master, text= 'add', command = self.addButton)
        add_button.grid(column = 1, row = 0)
        mainloop()
    
    
    def addButton(self):
        self.buttons_list.append('b'+str(len(self.buttons_list)+1))
        print(self.buttons_list)
        buttons = self.master.nametowidget('buttons')
        new_button = Button(buttons, text= self.buttons_list[-1])
        new_button.grid()
        buttons.update()
        
    def createButton(self, container):
        frame = Frame(container, name = "buttons")
        rows = 0
        
        for item in self.buttons_list:
            button = Button(frame, text = item)
            button.grid(column = 0, row = rows)
            rows += 1
    
        return frame


if __name__ == "__main__":
    App()