import tkinter
from tkinter import ttk
from workout2 import Workout

class fitnessTracker:
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



        #creates tabs for the application
        self.home_Tab()
        self.profile_Tab()
        self.createLog_Tab()
        self.viewLog_Tab()

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

        nameLabel = tkinter.Label(self.profileTab,text="name")
        nameLabel.pack()
        self.nameEntry = tkinter.Entry(self.profileTab,width=30)
        self.nameEntry.pack()

        val = tkinter.IntVar()
        val.set(0)

        mButton = tkinter.Radiobutton(self.profileTab,text="male",variable=val, value=0)
        fButton = tkinter.Radiobutton(self.profileTab,text="female",variable=val, value=1)
        mButton.pack()
        fButton.pack()

        ageLabel = tkinter.Label(self.profileTab,text="age")
        ageLabel.pack()
        self.ageEntry = tkinter.Entry(self.profileTab,width=10)
        self.ageEntry.pack()

        heightLabel = tkinter.Label(self.profileTab,text="height")
        heightLabel.pack()
        self.heightEntry = tkinter.Entry(self.profileTab,width=10)
        self.heightEntry.pack()

        weightLabel = tkinter.Label(self.profileTab,text="weight")
        weightLabel.pack()
        self.weightEntry = tkinter.Entry(self.profileTab,width=10)
        self.weightEntry.pack()

        profileSaveButton = tkinter.Button(self.profileTab, text="Save Profile", command= self.outputprofile)
        profileSaveButton.pack()
        
        homeButton = tkinter.Button(self.profileTab, text="Home", command=lambda: self.my_notebook.select(0))
        homeButton.pack(side=tkinter.BOTTOM, pady=5)


    def createLog_Tab(self):
        self.createLogTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.createLogTab, text= "log workouts")

        nameLabel = tkinter.Label(self.createLogTab,text="workout name")
        nameLabel.pack()
        self.nameEntry = tkinter.Entry(self.createLogTab,width=30)
        self.nameEntry.pack()

        setLabel = tkinter.Label(self.createLogTab,text="sets")
        setLabel.pack()
        sets = [1,2,3,4,5,6,7,8,9,10]
        setscb = ttk.Combobox(self.createLogTab, values=sets)
        setscb.pack()

        repLabel = tkinter.Label(self.createLogTab,text="reps")
        repLabel.pack()
        reps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        repscb = ttk.Combobox(self.createLogTab, values=reps)
        repscb.pack()

        weightLabel = tkinter.Label(self.createLogTab,text="weights(0 if none)")
        weightLabel.pack()
        weights = [0, 5, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0]
        weightcb = ttk.Combobox(self.createLogTab, values=weights)
        weightcb.pack()

        saveButton = tkinter.Button(self.createLogTab, text="Select Fruit", command=self.outputWorkout)
        saveButton.pack()

        homeButton = tkinter.Button(self.createLogTab, text="Home", command=lambda: self.my_notebook.select(0))
        homeButton.pack(side=tkinter.BOTTOM, pady=5)


    def viewLog_Tab(self):
        self.viewLogTab = tkinter.Frame(self.my_notebook)
        self.my_notebook.add(self.viewLogTab, text= "View Logs")

        homeButton = tkinter.Button(self.viewLogTab, text="Home", command=lambda: self.my_notebook.select(0))
        homeButton.pack(side=tkinter.BOTTOM, pady=5)


        return
        
    def outputWorkout(self):
        name = self.nameEntry.get()
        return name


    def outputprofile(self):
        print("Your profile is currently set to the following:",self.profileTab.get())



if __name__ == "__main__":
    root = tkinter.Tk()
    app = fitnessTracker(root)
    root.mainloop()