import tkinter
from tkinter import ttk
from workout2 import Workout
from workoutNames import workoutNames

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

        self.dynamic_frame = tkinter.Frame(self.createLogTab)
        self.dynamic_frame.pack(fill='x', padx=10, pady=10)

        self.add_button = tkinter.Button(self.createLogTab, text="Add Workout", command=self.add_workout_row)
        self.add_button.pack(pady=10)

        self.dropdown_options = workoutNames()

        self.row_counter = 0
        self.rows = []
        self.workouts = []


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
 
    def add_workout_row(self):
        """Add a new row for workout name"""
        # Create a frame for the row
        workout_frame = tkinter.Frame(self.dynamic_frame, bd=2, relief='groove')
        workout_frame.pack(fill='x', pady=5)

        self.nameLabel = tkinter.Label(workout_frame,text="workout name")
        self.nameLabel.pack(side='left', padx=5)

        # Create a dropdown (Combobox)
        dropdown_var = tkinter.StringVar()
        dropdown = ttk.Combobox(workout_frame, textvariable=dropdown_var, width=20, state="normal")
        dropdown.pack(side='left', padx=5)
        dropdown['values'] = self.dropdown_options  

        def on_dropdown_type(*args):
            current_text = dropdown_var.get()
            filtered_options = [
                option for option in self.dropdown_options if current_text.lower() in option.lower()
            ]
            dropdown['values'] = filtered_options

            # Keep the current text in the dropdown
            if current_text not in filtered_options:
                dropdown_var.set(current_text)

            # Attach filtering logic to the dropdown's text variable
        dropdown_var.trace_add("write", on_dropdown_type)

        add_set_button = tkinter.Button(workout_frame, text="Add Set", command=lambda: self.add_set_row(workout_frame))
        add_set_button.pack(side='left', padx=5)

        delete_workout_button = tkinter.Button(
            workout_frame,
            text="Delete Workout",
            command=lambda: self.delete_workout_row(workout_frame)
        )
        delete_workout_button.pack(side='left', padx=5)
        self.workouts.append({"frame": workout_frame, "sets": []})

    def add_set_row(self, workout_frame):
        """Add a new row for a new sets with reps and weights."""
        for workout in self.workouts:
            if workout["frame"] == workout_frame:
                set_frame = tkinter.Frame(workout_frame)
                set_frame.pack(fill='x', padx=20, pady=2)

                repLabel = tkinter.Label(set_frame,text="reps")
                repLabel.pack(side='left', padx=5)
                reps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
                repscb = ttk.Combobox(set_frame, values=reps)
                repscb.pack(side='left', padx=5)
        
                weightLabel = tkinter.Label(set_frame,text="weights(0  none)")
                weightLabel.pack(side='left', padx=5)
                weights = [0, 5, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0]
                weightcb = ttk.Combobox(set_frame, values=weights)
                weightcb.pack(side='left', padx=5)
        
                delete_set_button = tkinter.Button(
                    set_frame,
                    text="Delete Set",
                    command=lambda: self.delete_set_row(workout, set_frame)
                )
                delete_set_button.pack(side='left', padx=5)
                workout["sets"].append(set_frame)
                break

    def delete_workout_row(self, workout_frame):
        """Delete a workout row and all its associated sets."""
        for workout in self.workouts:
            if workout["frame"] == workout_frame:
                # Remove all set frames
                for set_frame in workout["sets"]:
                    set_frame.destroy()

                # Remove the workout frame
                workout_frame.destroy()

                # Remove from tracking list
                self.workouts.remove(workout)
                break

    def delete_set_row(self, workout, set_frame):
        """Delete a specific set row."""
        # Remove the set frame from the workout's tracking list
        if set_frame in workout["sets"]:
            workout["sets"].remove(set_frame)

        # Destroy the set frame
        set_frame.destroy()


if __name__ == "__main__":
    root = tkinter.Tk()
    app = fitnessTracker(root)
    root.mainloop()
