import tkinter
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from workout import Workout
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
        quitButton.pack(side=LEFT, expand= True, fill=BOTH)
        homeButton = ttk.Button(self.root, text="Home", command=lambda: self.my_notebook.select(0), bootstyle=SECONDARY)
        homeButton.pack(side=LEFT, expand= True, fill=BOTH)
        

        # Dictionary to store profiles based off name
        self.profiles = {}
        #dictionary to store all workouts
        self.workouts = {}
        #variable to keep track of what the current profile is
        self.currentProfile = ''

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

    #creates profile tab of application
    def profile_Tab(self):
        #initiates the window and configures the layout
        self.profileTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.profileTab, text= "Log Profile")
        self.profileTab.columnconfigure((0), weight = 1, uniform = 'a')
        self.profileTab.columnconfigure((1), weight = 2, uniform = 'a')
        self.profileTab.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight = 1, uniform = 'a')

        #creats a label indicating to the user that one can create a new profile
        newprofileLabel = tkinter.Label(self.profileTab,text="Enter the requested information \nbelow to create a new profile",  font=("Helvetica", 12, "bold"))
        newprofileLabel.grid(row=0, column =0, rowspan=2)

        #creates a spot to enter name
        nameLabel = tkinter.Label(self.profileTab,text="Name")
        nameLabel.grid(row=2, column =0, sticky='nsew')
        self.nameEntry = tkinter.Entry(self.profileTab,width=30)
        self.nameEntry.grid(row=3, column =0, sticky='ns')
        

        #allows user to enter a gender
        self.gender = tkinter.IntVar()
        self.gender.set(0)

        mButton = tkinter.Radiobutton(self.profileTab,text="male",variable=self.gender, value=0)
        fButton = tkinter.Radiobutton(self.profileTab,text="female",variable=self.gender, value=1)
        mButton.grid(row=4, column =0, sticky='nsew')
        fButton.grid(row=5, column =0, sticky='nsew')

        #allows user to enter age
        ageLabel = tkinter.Label(self.profileTab,text="age")
        ageLabel.grid(row=6, column =0, sticky='nsew')
        self.ageEntry = tkinter.Entry(self.profileTab,width=10)
        self.ageEntry.grid(row=7, column =0, sticky='ns')

        #allows user to enter height
        heightLabel = tkinter.Label(self.profileTab,text="Height(in)")
        heightLabel.grid(row=8, column =0, sticky='nsew')
        self.heightEntry = tkinter.Entry(self.profileTab,width=10)
        self.heightEntry.grid(row=9, column =0, sticky='ns')
        
        #allows user to enter weight
        weightLabel = tkinter.Label(self.profileTab,text="Weight(lbs)")
        weightLabel.grid(row=10, column =0, sticky='nsew')
        self.weightEntry = tkinter.Entry(self.profileTab,width=10)
        self.weightEntry.grid(row=11, column =0, sticky='ns')

        #creates a button to save current profile entries
        profileSaveButton = ttk.Button(
            self.profileTab,
            text="Save Profile", 
            command= lambda: func.saveProfile(self), 
            bootstyle=SUCCESS
            )
        profileSaveButton.grid(row=12, column =0, sticky='nsew')

        #creates button that outputs a profile
        outputButton = tkinter.Button(self.profileTab, text="Output Profiles", command= lambda: func.outputProfile(self))
        outputButton.grid(row=13, column =0, sticky='nsew')

        
        #creates a section where user can choose current profile and output their bmi and bmi category
        currentprofileLabel= tkinter.Label(self.profileTab, text="Current Profile:",font=("Helvetica", 16, "bold"))
        currentprofileLabel.grid(row=0, column=1)

        self.currentuserprofileLabel = tkinter.Label(self.profileTab, text= self.currentProfile,font=("Helvetica", 14, "bold"))
        self.currentuserprofileLabel.grid(row=1,column=1)

        setcurrentprofileLabel = tkinter.Label(self.profileTab,text="If you wish to change profiles, type in the profile name below")
        setcurrentprofileLabel.grid(row=2, column =1)


        #creates a frame to place these two widgets next to each other in the same grid celll
        currentprofileFrame = ttk.Frame(self.profileTab)
        currentprofileFrame.grid(row=3, column=1)  

        self.currentProfileEntry = tkinter.Entry(currentprofileFrame, width=10)
        self.currentProfileEntry.grid(row=0, column=0)  

        setcurrentprofileButton = ttk.Button(currentprofileFrame, text="Set profile", command=lambda: func.setProfile(self))
        setcurrentprofileButton.grid(row=0, column=1) 

        # self.currentProfileEntry = tkinter.Entry(self.profileTab,width=10)
        # self.currentProfileEntry.grid(row=3, column =1)
        # setcurrentprofileButton = ttk.Button(self.profileTab, text="Set profile", command= lambda:func.setProfile(self))
        # setcurrentprofileButton.grid(row=3,column=2,)

        bmiOutputButton = tkinter.Button(
            self.profileTab, 
            text="Click here to see your BMI and BMI category based off your profile", 
            command= lambda: func.bmiLevel(self,func.getBMI(self,self.currentProfileEntry.get())) 
            )
        bmiOutputButton.grid(row=4, column =1)

    #creates create log tab of application
    def createLog_Tab(self):
        self.createLogTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.createLogTab, text= "Log Workouts")
        
        #creates a table for the logs
        self.dynamic_frame = tkinter.Frame(self.createLogTab)
        self.dynamic_frame.pack(fill='x', padx=10, pady=10)

        self.add_excercise_button = tkinter.Button(self.createLogTab, text="Add excercise", command=lambda: func.add_excercise_row(self))
        self.add_excercise_button.pack(pady=10)

        self.dropdown_options = func.excerciseNames()

        save_button = tkinter.Button(self.createLogTab, text="Save", command= lambda: func.save_data(self))
        save_button.pack(side='bottom', padx=5)

        self.row_counter = 0
        self.rows = []
        self.excercises = []

    #creates view log tab of application
    def viewLog_Tab(self):
        self.viewLogTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.viewLogTab, text= "View Logs")

    #creates suggestions tab of application     
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

        send_button = ttk.Button(entry_frame, text="Send", command=lambda: func.handle_user_input(self,entry, text_widget))
        send_button.pack(side=tkinter.RIGHT)


