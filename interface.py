import tkinter
from tkinter import ttk
from workout2 import Workout
import functions as func

class GUI:
    def __init__(self, root):
        #initiates the GUI 
        self.root = root 
        self.root.title("Fitness Tracker")
        self.root.geometry("1000x500")

        #uses notebook to streamline tab usage
        self.my_notebook= ttk.Notebook(root)
        self.my_notebook.pack(expand=1,fill=tkinter.BOTH)
        quitButton = tkinter.Button(self.root, text="Quit", command=self.root.destroy)
        quitButton.pack()

        # Dictionary to store profiles based off name
        self.profiles = {}

        #creates tabs for the application
        self.home_Tab()
        self.profile_Tab()
        self.createLog_Tab()
        self.viewLog_Tab()

        self.data = []

    #creates the home tab of the application
    def home_Tab(self):
        self.home_tab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.home_tab, text= "Home")

        #add two labels that welcome the user to the program and explains how to use it
        welcomeLabel = tkinter.Label(self.home_tab, text="Welcome to your Personal Fitness Tracker!")
        welcomeLabel.pack()
        navigateLabel = tkinter.Label(self.home_tab, text="Please use the following buttons to navigate through the program!")
        navigateLabel.pack()

        #creates three buttons that lead to each corresponding tab
        profileButton = tkinter.Button(self.home_tab, text="Profile", command=lambda: self.my_notebook.select(1) )
        profileButton.pack(pady=5)
        createLogButton = tkinter.Button(self.home_tab, text="Create a new log", command=lambda: self.my_notebook.select(2))
        createLogButton.pack(pady=5)
        viewLogButton = tkinter.Button(self.home_tab, text="View your previous logs", command=lambda: self.my_notebook.select(3))
        viewLogButton.pack(pady=5)

    def profile_Tab(self):
        self.profileTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.profileTab, text= "log profile")
        self.profileTab.grid_columnconfigure(1, weight=1)

        nameLabel = tkinter.Label(self.profileTab,text="name")
        nameLabel.pack(side = "top", anchor= "nw")
        self.nameEntry = tkinter.Entry(self.profileTab,width=30)
        self.nameEntry.pack(side = "top", anchor= "nw")

        self.gender = tkinter.IntVar()
        self.gender.set(0)

        mButton = tkinter.Radiobutton(self.profileTab,text="male",variable=self.gender, value=0)
        fButton = tkinter.Radiobutton(self.profileTab,text="female",variable=self.gender, value=1)
        mButton.pack(side = "top", anchor= "nw")
        fButton.pack(side = "top", anchor= "nw")

        ageLabel = tkinter.Label(self.profileTab,text="age")
        ageLabel.pack(side = "top", anchor= "nw")
        self.ageEntry = tkinter.Entry(self.profileTab,width=10)
        self.ageEntry.pack(side = "top", anchor= "nw")

        heightLabel = tkinter.Label(self.profileTab,text="Height(in)")
        heightLabel.pack(side = "top", anchor= "nw")
        self.heightEntry = tkinter.Entry(self.profileTab,width=10)
        self.heightEntry.pack(side = "top", anchor= "nw")

        weightLabel = tkinter.Label(self.profileTab,text="Weight(lbs)")
        weightLabel.pack(side = "top", anchor= "nw")
        self.weightEntry = tkinter.Entry(self.profileTab,width=10)
        self.weightEntry.pack(side = "top", anchor= "nw")

        profileSaveButton = tkinter.Button(self.profileTab, text="Save Profile", command= lambda: func.saveProfile(self))
        profileSaveButton.pack(side = "top", anchor= "nw")

        #creates button that outputs a profile
        outputButton = tkinter.Button(self.profileTab, text="Output Profile", command= lambda: func.outputProfile(self))
        outputButton.pack(side = "top", anchor= "nw",pady=5)
        
        #creates a section where user can choose current profile and output their bmi and bmi category
        profileLabel = tkinter.Label(self.profileTab,text="Select the profile you wish to continue with")
        profileLabel.pack(side ="top", anchor= "center")
        self.currentProfileEntry = tkinter.Entry(self.profileTab,width=10)
        self.currentProfileEntry.pack(side ="top", anchor= "center")
        bmiOutputButton = tkinter.Button(self.profileTab, text="Click here to see your BMI and BMI category based off your profile", command= lambda: func.bmiLevel(self,func.getBMI(self,self.currentProfileEntry.get())) )
        bmiOutputButton.pack(side = "top", anchor = "center", pady=5)
        
        #creates button that takes user back to home
        homeButton = tkinter.Button(self.profileTab, text="Home", command=lambda: self.my_notebook.select(0))
        homeButton.pack(side=tkinter.BOTTOM, pady=5)


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

        self.tree = ttk.Treeview(self.viewLogTab, columns=("Workout", "rep", "weight"), show="headings")
        self.tree.heading("Workout", text="Workout")
        self.tree.heading("rep", text="rep")
        self.tree.heading("weight", text="weight")
        self.tree.pack(fill="both", expand=True)

        homeButton = tkinter.Button(self.viewLogTab, text="Home", command=lambda: self.my_notebook.select(0))
        homeButton.pack(side=tkinter.BOTTOM, pady=5)

     
