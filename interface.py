import tkinter
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from workout2 import Workout
import functions as func

class GUI:
    def __init__(self, root):
        #initiates the GUI 
        self.root = root 
        self.root.title("Fitness Tracker")
        self.root.geometry("1500x900")

        #uses notebook to streamline tab usage
        self.my_notebook= ttk.Notebook(root, bootstyle=PRIMARY)
        self.my_notebook.pack(expand=1,fill=tkinter.BOTH)
        quitButton = ttk.Button(self.root, text="Quit", command=self.root.destroy, bootstyle=DANGER)
        quitButton.pack()

        # Dictionary to store profiles based off name
        self.profiles = {}

        #creates tabs for the application
        self.home_Tab()
        self.profile_Tab()
        self.createLog_Tab()
        self.viewLog_Tab()
        self.suggestions_Tab()

        self.data = []

    #creates the home tab of the application
    def home_Tab(self):
        self.home_tab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.home_tab, text= "Home")

        #add two labels that welcome the user to the program and explains how to use it
        welcomeLabel = tkinter.Label(self.home_tab, text="Welcome to your Personal Fitness Tracker!", font=("Helvetica", 18, "bold") )
        welcomeLabel.pack(pady=10)
        navigateLabel = tkinter.Label(self.home_tab, text="Please use the following buttons to navigate through the program!")
        navigateLabel.pack(pady=5)

        #creates buttons that lead to each corresponding tab
        profileButton = tkinter.Button(self.home_tab, text="Profile", command=lambda: self.my_notebook.select(1) )
        profileButton.pack(pady=10)
        createLogButton = tkinter.Button(self.home_tab, text="Create a new log", command=lambda: self.my_notebook.select(2))
        createLogButton.pack(pady=10)
        viewLogButton = tkinter.Button(self.home_tab, text="View your previous logs", command=lambda: self.my_notebook.select(3))
        viewLogButton.pack(pady=10)
        suggestionButton = tkinter.Button(self.home_tab, text="Request an excercise suggestion", command=lambda: self.my_notebook.select(4))
        suggestionButton.pack(pady=10)

    def profile_Tab(self):
        self.profileTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.profileTab, text= "Log Profile")
        self.profileTab.columnconfigure((0,1), weight = 1, uniform = 'a')
        self.profileTab.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight = 1, uniform = 'a')

        #creates a spot to enter name
        nameLabel = tkinter.Label(self.profileTab,text="Name")
       # nameLabel.pack(side = "top", anchor= "nw")
        nameLabel.grid(row=0, column =0)
        self.nameEntry = tkinter.Entry(self.profileTab,width=30)
        #self.nameEntry.pack(side = "top", anchor= "nw")
        self.nameEntry.grid(row=1, column =0)
        

        #allows user to enter a gender
        self.gender = tkinter.IntVar()
        self.gender.set(0)

        mButton = tkinter.Radiobutton(self.profileTab,text="male",variable=self.gender, value=0)
        fButton = tkinter.Radiobutton(self.profileTab,text="female",variable=self.gender, value=1)
        #mButton.pack(side = "top", anchor= "nw")
        #fButton.pack(side = "top", anchor= "nw")
        mButton.grid(row=2, column =0)
        fButton.grid(row=3, column =0)

        #allows user to enter age
        ageLabel = tkinter.Label(self.profileTab,text="age")
        #ageLabel.pack(side = "top", anchor= "nw")
        ageLabel.grid(row=4, column =0)
        self.ageEntry = tkinter.Entry(self.profileTab,width=10)
        #self.ageEntry.pack(side = "top", anchor= "nw")
        self.ageEntry.grid(row=5, column =0)

        #allows user to enter height
        heightLabel = tkinter.Label(self.profileTab,text="Height(in)")
       # heightLabel.pack(side = "top", anchor= "nw")
        heightLabel.grid(row=6, column =0)
        self.heightEntry = tkinter.Entry(self.profileTab,width=10)
        #self.heightEntry.pack(side = "top", anchor= "nw")
        self.heightEntry.grid(row=7, column =0)
        

        
        #allows user to enter weight
        weightLabel = tkinter.Label(self.profileTab,text="Weight(lbs)")
        #weightLabel.pack(side = "top", anchor= "nw")
        weightLabel.grid(row=8, column =0)
        self.weightEntry = tkinter.Entry(self.profileTab,width=10)
        #self.weightEntry.pack(side = "top", anchor= "nw")
        self.weightEntry.grid(row=9, column =0)

        #creates a button to save current profile entries
        profileSaveButton = ttk.Button(
            self.profileTab,
            text="Save Profile", 
            command= lambda: func.saveProfile(self), 
            bootstyle=SUCCESS
            )
        #profileSaveButton.pack(side = "top", anchor= "nw")
        profileSaveButton.grid(row=10, column =0)

        #creates button that outputs a profile
        outputButton = tkinter.Button(self.profileTab, text="Output Profile", command= lambda: func.outputProfile(self))
        #outputButton.pack(side = "top", anchor= "nw",pady=5)
        outputButton.grid(row=11, column =0)

        
        #creates a section where user can choose current profile and output their bmi and bmi category
        profileLabel = tkinter.Label(self.profileTab,text="Select the profile you wish to continue with")
        #profileLabel.pack(side ="top", anchor= "center")
        profileLabel.grid(row=0, column =1)

        self.currentProfileEntry = tkinter.Entry(self.profileTab,width=10)
        #self.currentProfileEntry.pack(side ="top", anchor= "center")
        self.currentProfileEntry.grid(row=1, column =1)

        bmiOutputButton = tkinter.Button(self.profileTab, text="Click here to see your BMI and BMI category based off your profile", command= lambda: func.bmiLevel(self,func.getBMI(self,self.currentProfileEntry.get())) )
        #bmiOutputButton.pack(side = "top", anchor = "center", pady=5)
        bmiOutputButton.grid(row=2, column =1)

        #creates button that takes user back to home
        homeButton = tkinter.Button(self.profileTab, text="Home", command=lambda: self.my_notebook.select(0))
        #homeButton.pack(side=tkinter.BOTTOM, pady=5)
        homeButton.grid(row=11, column =1)


    def createLog_Tab(self):
        self.createLogTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.createLogTab, text= "log workouts")

        self.dynamic_frame = tkinter.Frame(self.createLogTab)
        self.dynamic_frame.pack(fill='x', padx=10, pady=10)

        self.add_button = tkinter.Button(self.createLogTab, text="Add Workout", command=lambda: func.add_workout_row(self))
        self.add_button.pack(pady=10)

        self.dropdown_options = func.workoutNames()

        save_button = tkinter.Button(self.createLogTab, text="Save", command= lambda: func.save_data(self))
        save_button.pack(side='bottom', padx=5)

        self.row_counter = 0
        self.rows = []
        self.workouts = []


    def viewLog_Tab(self):
        self.viewLogTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.viewLogTab, text= "View Logs")

        self.tree = ttk.Treeview(self.viewLogTab, columns=("Excercise", "rep", "weight"), show="headings")
        self.tree.heading("Excercise", text="Excercise")
        self.tree.heading("rep", text="rep")
        self.tree.heading("weight", text="weight")
        self.tree.pack(fill="both", expand=True)

        homeButton = tkinter.Button(self.viewLogTab, text="Home", command=lambda: self.my_notebook.select(0))
        homeButton.pack(side=tkinter.BOTTOM, pady=5)

     
    def suggestions_Tab(self):
        self.suggestionsTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.suggestionsTab, text= "Request suggestions")

        suggestionLabel = tkinter.Label(self.suggestionsTab, text="Below you can ask questions relating to fitness and the fitness companion will answer them. ")
        suggestionLabel.pack()

        text_widget = tkinter.Text(self.suggestionsTab, wrap=tkinter.WORD, height=20, width=50)
        text_widget.pack(padx=10, pady=10)

        # Add an Entry widget for user input
        entry_frame = ttk.Frame(self.suggestionsTab)
        entry_frame.pack(fill=tkinter.X, padx=10, pady=10)

        entry = ttk.Entry(entry_frame)
        entry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=(0, 10))
        entry.focus()

        send_button = ttk.Button(entry_frame, text="Send", command=lambda: self.handle_user_input(entry, text_widget))
        send_button.pack(side=tkinter.RIGHT)

        homeButton = tkinter.Button(self.suggestionsTab, text="Home", command=lambda: func.my_notebook.select(0))
        homeButton.pack(side=tkinter.BOTTOM, pady=5)
