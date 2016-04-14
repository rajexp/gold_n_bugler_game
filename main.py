#!/usr/bin/env python
from tkinter import *
import tkinter.font, random, math
from tkinter import ttk
position=[]
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
def page(self):
    label = ttk.Label(self, text="Start game?", font=LARGE_FONT)
    button1 = ttk.Button(self, text="Agree", command=self.begin)
    button2 = ttk.Button(self, text="Disagree",command=quit)
 
    label.pack()
    button1.pack()
    button2.pack()
 
 
class MyWindow(Frame):
    def __init__(self, master):
        global position
 
        super(MyWindow, self).__init__()
        self.widgets={}
 
       
        self.app = Frame(master, bg="yellow")
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_columnconfigure(0, weight=1)
        self.app.pack(fill="both", expand=True)
     
        # instructions and fonts
        self.mono_font = tkinter.font.Font(family="Courier",size=24,weight="bold")
        self.instructions = "Find the hidden treasure!\n\nUse the arrow keys to select where to look, then press Enter to check. \
        There is a 50/50 chance you will be told the distance from the treasure. Keep hunting until you find it. Good luck!"
        # create instructions widget
        self.info = Text(self.app, wrap=WORD, padx=10, pady=10,width=15,bd=0, height=19, bg="yellow")
        self.info.insert(1.0,self.instructions)
        self.info.grid(row=0,column=0,columnspan=2,sticky=N+E+S+W)
        self.info.config(state=DISABLED)
        # create island widget
        self.island = Text(self.app, bg="cyan", padx=40, pady=80, font=self.mono_font,width=20, height=10, wrap=NONE,bd=0)
        self.island.insert(1.0, "ready")
        self.island.grid(row=0,column=3,rowspan=6, stick=N+E+S+W,)      
        # Input for grid size and treasure and bandits]
        self.grid_size_label = Label(self.app,bg="yellow",text="Grid-Size")
        self.grid_size_label.grid(row=2,column=0,padx=2)
        self.grid_size_var=StringVar(self.app)
        self.grid_size_var.set("small") # initial value
        self.grid_size = OptionMenu(self.app,self.grid_size_var, "small", "medium", "large",)
        self.grid_size.grid(row=2,column=1,padx=10,pady=5)
        #Options for NO of Treasures
        Treasure_Options=[i for i in range(1,11)]
        self.treasure_size_label = Label(self.app,bg="yellow",text="Treasures")
        self.treasure_size_label.grid(row=3,column=0,padx=2)
        self.treasure_size_var=StringVar(self.app)
        self.treasure_size_var.set(Treasure_Options[4])
        self.treasure_size=OptionMenu(self.app,self.treasure_size_var,*Treasure_Options)
        self.treasure_size.grid(row=3,column=1,padx=10,pady=5)
         #Options for NO of Bandit
        Bandit_Options=[i for i in range(1,11)]
        self.bandit_size_label = Label(self.app,bg="yellow",text="Bandits")
        self.bandit_size_label.grid(row=4,column=0,padx=2)
        self.bandit_size_var=StringVar(self.app)
        self.bandit_size_var.set(Bandit_Options[4])
        self.bandit_size=OptionMenu(self.app,self.bandit_size_var,*Bandit_Options)
        self.bandit_size.grid(row=4,column=1,padx=10,pady=5)
        # menu buttons
        
        self.start_a = Button(self.app, text="Start game", bg="red", command=self.start)
        self.start_a.grid(row=5, column=0,columnspan=2, pady=5)
        self.start_b = Button(self.app, text="Quit game", bg="red", command=quit)
        self.start_b.grid(row=6, column=0,columnspan=2, pady=5)
       
        # score labels and fields
        self.score_lbl = Label(self.app, text="Guesses: 0", bg="yellow")
        self.score_lbl.grid(row=1, column=0,padx=5,columnspan=2,sticky=W+N)
 
        # set keydown handler
        root.bind("<Key>", self.key_pressed)
        # best score variable
        self.Found=False
        self.best_score = 0
        self.score=0
        self.grid_limit= 6
        self.avaliable_pos=position
        # begin game
        #self.page()
        #print self.treasure_pos
       
    def start(self):
        self.start_a['text']='  Restart  ' if (self.start_a['text'])=='Start game' else 'Start game'
        self.start_a['command']=self.restart
        # HIding Options Since game has started 
        self.treasure_size_label.grid_forget()
        self.bandit_size_label.grid_forget()
        self.grid_size_label.grid_forget()
        self.treasure_size.grid_forget()
        self.bandit_size.grid_forget()
        self.grid_size.grid_forget()
        # Appearing Score Label so that score can be seen 
        self.treasure_score= Label(self.app,bg="yellow",text="Treasure Found : 0")
        self.treasure_score.grid(row=2,column=0,padx=2,columnspan=2,sticky=N+W)
        self.score_label= Label(self.app,bg="yellow",text="Score : 0")
        self.score_label.grid(row=3,column=0,padx=2,columnspan=2,sticky=N+W)
        self.begin()
    def restart(self):
        # ON Restart Change the text to Start Game
        self.start_a['text']='  Restart  ' if (self.start_a['text'])=='Start game' else 'Start game'
        self.start_a['command']=self.start
        # HIding score
        self.score_label.grid_forget()
        self.treasure_score.grid_forget()
        # REappear of Option Menu
        self.grid_size_label.grid(row=2,column=0,padx=2)
        self.grid_size.grid(row=2,column=1,padx=10,pady=5)
        self.treasure_size_label.grid(row=3,column=0,padx=2)
        self.treasure_size.grid(row=3,column=1,padx=10,pady=5)
        self.bandit_size.grid(row=4,column=1,padx=10,pady=5)
        self.bandit_size_label.grid(row=4,column=0,padx=2)
    def begin(self):
        global position
        if self.grid_size_var.get()=="small":
            self.grid_limit=6
            position=[[i,j] for i in range(0,6) for j in range(0,6)]         
            self.matrix = [["#" for col in range(6)] for row in range(6)]
            self.current_pos = [random.randrange(6), random.randrange(6)]
        elif self.grid_size_var.get()=="medium":
            self.grid_limit=8
            position=[[i,j] for i in range(0,8) for j in range(0,8)]
            self.matrix = [["#" for col in range(8)] for row in range(8)]
            self.current_pos = [random.randrange(8), random.randrange(8)]
        elif self.grid_size_var.get()=="large":
            self.grid_limit=10
            position=[[i,j] for i in range(0,10) for j in range(0,10)]
            self.matrix = [["#" for col in range(10)] for row in range(10)]
            self.current_pos = [random.randrange(10), random.randrange(10)]
        print(self.current_pos)
        # game state variables
        root.after_cancel(self.tick)
        position.remove(self.current_pos)
        # Generate Treasure Position
        self.treasure_pos = list(random.sample(list(position),int(self.treasure_size_var.get())))
        for pos in self.treasure_pos:
            position.remove(pos)
            #Generate Bandit Position
        self.bandit_pos = list(random.sample(list(position),int(self.bandit_size_var.get())))
        print (self.treasure_pos)
        print (self.bandit_pos)
        self.blink = False
        self.guesses = 0
        self.treasure_found = 0
        self.end_tick = False
        self.tick()
        self.Found=False
 
    def display_grid(self):
        '''Displays current visual game state'''
        self.island.delete(1.0, END)
        m_str = ""
        for row in range(len(self.matrix)):
            m_str += (" ".join(self.matrix[row]) + "\n")
        self.island.insert(1.0, m_str)
 
    def process_guess(self):
        self.guesses += 1
        self.score_lbl.config(text="Guesses: " + str(self.guesses))
        if self.current_pos not in self.treasure_pos and  self.current_pos not in self.bandit_pos: #NOT A TREASURE LOCATION
            print ("NOT HERE")
            # Calculating Nearest Distance but we haven't shown this distance anywhere so don't know what's the use here
             #YOu can show this nearest distance in a label for user
            if len(self.treasure_pos)>0:
                dist = min(int(round(math.sqrt((self.current_pos[0] - self.treasure_pos[i][0]) ** 2 + (self.current_pos[1] - self.treasure_pos[i][1]) ** 2))) for i in range(len(self.treasure_pos)))
            else:
                dist = 0
            self.display_grid()
        elif self.current_pos in self.bandit_pos:
            self.score=0
            self.matrix[self.current_pos[0]][self.current_pos[1]]='B'
            # REMOVE THE TREASURE FROM THE REMAINING TREASURE LIST
            self.bandit_pos.remove(self.current_pos)
            self.end_tick = True
            self.tick()
        elif self.current_pos in self.treasure_pos: # TREASURE LOCATION FOUND
            # 10 Gold COllected 
            self.score+=10
            # PUT $ sign since GOLD IS FOUND
            self.matrix[self.current_pos[0]][self.current_pos[1]]='$'
            # REMOVE THE TREASURE FROM THE REMAINING TREASURE LIST
            self.treasure_pos.remove(self.current_pos)
            self.treasure_found+=1
            self.treasure_score.config(text="Treasure Found : "+str(self.treasure_found))
            self.end_tick = True
            print(self.treasure_size_var.get())
            print (self.treasure_found)
            # IF treasure found equals the total treasures in grid then print that all treasure has been found 
            if self.treasure_found==int(self.treasure_size_var.get()):
                self.treasure_score.config(text="All Treasure Found .")
                self.score_lbl.config(text="Win in " + str(self.guesses)+" Guesses")
            self.tick()
        self.score_label.config(text="Score : "+str(self.score))
    
            
 
    def tick(self):
        '''timer for blinking cursor'''
        if not (self.matrix[self.current_pos[0]][self.current_pos[1]] == "$" or self.matrix[self.current_pos[0]][self.current_pos[1]] == "B") :
            if self.blink == False:
                self.matrix[self.current_pos[0]][self.current_pos[1]] = "#"
            elif self.blink == True and self.Found:
                self.matrix[self.current_pos[0]][self.current_pos[1]] = "$"
            elif self.blink == True :
                self.matrix[self.current_pos[0]][self.current_pos[1]] = " "
        else:
            pass
        self.blink = not self.blink
        self.display_grid()
        root.after(200, self.tick)
 
    def key_pressed(self, event):
        # If the gold was there earlier then don't blink or change the symbol of that location 
        if self.Found==False and not (self.matrix[self.current_pos[0]][self.current_pos[1]] == "$" or self.matrix[self.current_pos[0]][self.current_pos[1]] == "B"):
            self.matrix[self.current_pos[0]][self.current_pos[1]] = "#"
        self.Found=False
        if event.keysym == "Right" and self.current_pos[1] < self.grid_limit-1:
            self.current_pos[1] += 1
        elif event.keysym == "Left" and self.current_pos[1] > 0:
            self.current_pos[1] -= 1
        elif event.keysym == "Up" and self.current_pos[0] > 0:
            self.current_pos[0] -= 1
        elif event.keysym == "Down" and self.current_pos[0] < self.grid_limit-1:
            self.current_pos[0] += 1
        elif event.keysym == "Return":
            self.process_guess()
        self.display_grid()
        
 
root = Tk()
root.title("We made this Game :P")
MyWindow(root).pack()
root.mainloop()
