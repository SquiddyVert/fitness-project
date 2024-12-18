# Authors: Samuel Franco and Dekang Lu
# Description: storing the complexity of several functions
import tkinter
from tkinter import ttk
from tkinter import messagebox
from profile_1 import Profile
from workout import Workout
from exercise import Exercise
from set import Set
from chatbot import find_most_similar_question
from datetime import datetime

def getBMI(GUI, name):
    '''calculates bmi based off user input height and weight
    :name p1: profile name for who the bmiis being checked
    :return: BMI'''
    if name in GUI.profiles:
        profile = GUI.profiles[name] 
        height = profile.getHeight() 
        weight = profile.getWeight() 
    try:
        BMI = (weight * 703) / (height ** 2)
        return BMI
    except ZeroDivisionError:
        return "Height cannot be zero."

def bmiLevel(GUI,BMI):
    '''function calculates what category of bmi the user is
    :BMI p1: the bmi of the user
    :return: a message saying what level of bmi the user is'''
    #if the label exissts already, it will be deleted before creating it again
    if hasattr(GUI, 'bmilevelLabel') and GUI.bmilevelLabel.winfo_exists():
        GUI.bmilevelLabel.destroy() 

    match BMI:
        case n if n < 18.5:
            bmilevelMessage = "According to the World Health Organization(WHO), \n your BMI level of", BMI, "means you are classified as Underweight"
        case n if 18.5 <= n < 24.9:
            bmilevelMessage = "According to the World Health Organization(WHO), \n your BMI level of", BMI, "means you are classified as Normal weight"
        case n if 25 <= n < 29.9:
            bmilevelMessage = "According to the World Health Organization(WHO), \n your BMI level of", BMI, "means you are classified as  Overweight"
        case n if n > 25:
            bmilevelMessage = "According to the World Health Organization(WHO), \n your BMI level of", BMI, "means you are classified as  Obese"
    
    bmilevelLabel = tkinter.Label(GUI.profileTab,text= bmilevelMessage)
    bmilevelLabel.grid(row=5, column=1)

def saveProfile(GUI):
    '''Grabs all the profile information and clear inputs after creating a profile'''
    #Grabs all the profile information
    name = GUI.nameEntry.get()
    age = int(GUI.ageEntry.get())
    height = float(GUI.heightEntry.get())
    weight = float(GUI.weightEntry.get())
    if GUI.gender.get() == 0:
        gender = "Male" 
    else:
        gender = "Female"
    
    #creates an instance of profile class and saves to a dictionary
    profile = Profile(name, gender, age, height, weight)
    GUI.profiles[name] = profile
    
    #Notifies user that the profile has been saved
    tkinter.messagebox.showinfo("Alert","Profile has been saved!")

    #clears all the information that was in the profile entries
    GUI.nameEntry.delete(0, tkinter.END)
    GUI.ageEntry.delete(0, tkinter.END)
    GUI.heightEntry.delete(0, tkinter.END)
    GUI.weightEntry.delete(0, tkinter.END)
    GUI.gender.set(0)

def outputProfile(GUI):
    '''Output and display collected profile information in detail'''
     #check whether or not htere are any profiles
    if  GUI.profiles == {}:
        tkinter.messagebox.showinfo("Profiles", "There are no profiles to display. Add your profile to see it displayed here!")
        return
    
    #turns into a string making it so every profile is a string of its own on a new line
    profilesMessage = "\n\n".join([
        f"Name: {profile.getName()}\n"
        f"Gender: {profile.getSex()}\n"
        f"Age: {profile.getAge()}\n"
        f"Height: {profile.getHeight()} in\n"
        f"Weight: {profile.getWeight()} lbs"
        for profile in GUI.profiles.values()
    ])
     
    tkinter.messagebox.showinfo(f"Profiles",f"All Saved Profiles: \n {profilesMessage}")    #outputs the saved profiles as an alert box

def setProfile(GUI):
    '''Check if there is a saved profile and enable user to select a profile if so'''
    #creates a variable for whatever name is currently in the text box
    updatedcurrentProfile = GUI.currentProfileEntry.get()

    # Check if the profile exists in the profiles dictionary, if so updates the currentprofile label and variable accordingly
    if updatedcurrentProfile in GUI.profiles:
        GUI.currentProfile = updatedcurrentProfile 
        GUI.currentuserprofileLabel.config(text=f"{GUI.currentProfile}")
    else:
        tkinter.messagebox.showinfo("Error", "Profile not found! Check 'output profiles' to see what profiles are availableto choose from")

def add_exercise_row(GUI):
    '''Adding a row for a new exercise entry'''
    # Create a frame for the row
    exercise_frame = tkinter.Frame(GUI.dynamic_frame, bd=2, relief='groove')
    exercise_frame.pack(fill='both', pady=5)

    nameLabel = tkinter.Label(exercise_frame,text="Exercise name")
    nameLabel.pack(side='left', padx=5)

    # Create a dropdown (Combobox)
    dropdown_var = tkinter.StringVar()
    dropdown = ttk.Combobox(exercise_frame, textvariable=dropdown_var, width=20, state="normal")
    dropdown.pack(side='left', padx=5)
    dropdown['values'] = GUI.dropdown_options 


    def on_dropdown_type(*args):
        """Function to enable changes on dropdown options based on entry (text variable)"""
        current_text = dropdown_var.get()
        filtered_options = [
            option for option in GUI.dropdown_options if current_text.lower() in option.lower()
        ]
        dropdown['values'] = filtered_options

        # Keep the current text in the dropdown
        if current_text not in filtered_options:
            dropdown_var.set(current_text)

    # Attach filtering logic to the dropdown's text variable
    dropdown_var.trace_add("write", on_dropdown_type)

    def on_dropdown_select(event):
        """Function to save the choice of exercise and add follow up buttons"""
        selectedOption = dropdown_var.get()
        
        #creates an instance of exercise and saves it to the workout instance
        newExercise = Exercise(name=selectedOption)
        GUI.currentWorkout.addExercise(newExercise)

        # the buttons are updated to be able to perform their actions 
        add_set_button.config(state="normal", command=lambda: add_set_row(GUI, exercise_frame, newExercise))
        delete_exercise_button.config(command=lambda: delete_exercise_row(GUI, exercise_frame, newExercise))


    # creates a bind on the dropdown
    dropdown.bind("<<ComboboxSelected>>",  on_dropdown_select)

    #creates an add set button that allows user to add set to exercise
    add_set_button = tkinter.Button(exercise_frame, text="Add Set", state= "disabled")
    add_set_button.pack(side='left', padx=5)

    #creates a delete button for the exercise
    delete_exercise_button = tkinter.Button(
        exercise_frame,
        text="Delete Exercise",
        command=lambda: delete_exercise_row(GUI, exercise_frame)
    )
    delete_exercise_button.pack(side='left', padx=5)

def add_set_row(GUI, exercise_frame, exercise):
    """Add a new row for a new sets with reps and weights.
    :exercise_frame: the frame that holds the individual exercise option
    :exercise: specific exercise class object"""
    #creates a new set frame for each set
    set_frame = tkinter.Frame(exercise_frame)
    set_frame.pack(fill='x', padx=20, pady=2) 

    #creates labels and widgets for reps and weigweightht
    repsLabel = tkinter.Label(set_frame,text="Reps")
    repsLabel.pack(side='left', padx=5)
    repsEntry = ttk.Entry(set_frame,width=10)
    repsEntry.pack(side='left', padx=5)
  
    weightLabel = tkinter.Label(set_frame,text="Weight (lbs)")
    weightLabel.pack(side='left', padx=5)
    weightEntry = ttk.Entry(set_frame, width=10)
    weightEntry.pack(side='left', padx=5)

    #creates a delete button for the set
    delete_set_button = tkinter.Button(
        set_frame,
        text="Delete Set",
        command=lambda: delete_set_row(GUI,set_frame, exercise)
    )
    delete_set_button.pack(side='right', padx=5)

    # variable to track if set has been saved and to prevent multiple saves
    saved = {"status": False}


    #function to handle the set values because by default they are empty
    def get_set_values(repsEntry, weightEntry):
        """Retrieve the values from the entry widgets and validate them.
        :repsEntry: entry storing reps input
        :weightEntry: entry storing weight input
        :return: reps and weight value from entry, 0 if none"""
        try:
            # Get the values from the entry fields
            reps = repsEntry.get()
            weight = weightEntry.get()

            # Checks if the value is empty and sets it to a default value of 0 if it is
            if not reps:
                reps = 0
            else:
                reps = int(reps)

            if not weight:
                weight = 0.0
            else:
                weight = float(weight)

            return reps, weight
        except ValueError:
            # In case of invalid input, set default values
            return 0, 0.0

    def setinputComplete():
        """checking if data is saved, if not, retrieve them from entries and store into set instance of the exercise object"""
        # checks if set has been saved already
        if saved["status"]:  
            return
        
        # Get the set values from the entries
        reps, weight = get_set_values(repsEntry, weightEntry)
   
        # Create a new Set instance
        newSet = Set(reps=reps, weight=weight)
    
        # Add the new set to the exercise
        exercise.addSet(newSet)

        #updates variable to mark that the set has been saved
        saved["status"] = True

        #configure delete button to actually work as intended once there is data in the entry fields
        delete_set_button.config(command=lambda: delete_exercise_row(GUI, exercise_frame, newSet))
        
    #creates a manual save set button that user must click in order to save the set to the workout
    save_set_button = tkinter.Button(
        set_frame,
        text="Save Set",
        command=setinputComplete  
    )
    save_set_button.pack(side='right', padx=5)

  
def delete_exercise_row(GUI, exercise_frame, exercise=None):
    """Delete an exercise row and all its associated sets.
    :exercise_frame: the frame that holds the individual exercise option
    :exercise: specific exercise class object, default as none if no input yet"""

    #deletes the exercise from the workoutinstance
    if exercise:
        for set in exercise.sets:
            set.frame.destroy()
        GUI.currentWorkout.exercises.remove(exercise)

    #deleted the exercise frame
    exercise_frame.destroy()

def delete_set_row(GUI,set_frame, exercise, set= None):
    """Delete an set row and all its associated sets.
    :set_frame: the frame that holds the individual set data
    :exercise: specific exercise class object, 
    :set: specific set instance, default as none if no input yet"""
    #deletes the set row
    set_frame.destroy()

    #deletes the set from the exercise instance
    if set:
        exercise.sets.remove(set)

def reset_log_tab(GUI):
    """Clear the Log Tab and reset it to its initial state."""
    # Destroy all widgets in the dynamic frame
    for widget in GUI.dynamic_frame.winfo_children():
        widget.destroy()

    # Creates a new instance of workout, ready to be used for a new workout log
    GUI.currentWorkout = Workout(date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def save_workout(GUI):
    """Save the current workout and sets to the data list and display them in the table."""
    if not GUI.currentProfile:
        tkinter.messagebox.showerror("Error", "Please select a profile before saving")
        return
    
    #saves the date of the workout
    workoutDate = GUI.currentWorkout.date

    #returns a summary of the whole workout 
    workoutSummary = GUI.currentWorkout.getSummary()

    #adds the workout summary to the workout log dictionary, with the date being the key
    GUI.workoutLogs[workoutDate] = workoutSummary

    #alerts the user that their workout has been saved and shows them the summary
    tkinter.messagebox.showinfo("Success",f"The following workout for {workoutDate} has been saved!\n {workoutSummary}")
    
    #calls the reset function 
    reset_log_tab(GUI)
    
    for widget in GUI.viewLogTab.winfo_children():
        widget.destroy()
    for time in GUI.workoutLogs:
        summary = GUI.workoutLogs.get(time)
        workout_frame = tkinter.Frame(GUI.viewLogTab)
        workout_frame.pack(fill='x', padx=20, pady=2)
        detailLabel = tkinter.Label(GUI.viewLogTab,text=f"{summary}")
        detailLabel.pack(side='left', padx=5)
    GUI.my_notebook.select(3)

def handle_user_input(GUI, entry, text_widget):
    """processing user entry in suggestion tab
    :entry: entry containing user input
    :text_widget: the widget displaying suggestions interactions"""
    user_input = entry.get()
    entry.delete(0, tkinter.END)

    if user_input.lower() == 'bye':
        text_widget.insert(tkinter.END, "Q&A support: Goodbye!\n")
        return

    response = find_most_similar_question(user_input)
    text_widget.insert(tkinter.END, f"You: {user_input}\n")
    text_widget.insert(tkinter.END, f"Q&A support: {response}\n\n")
    text_widget.see(tkinter.END)

def exerciseNames():
    """function just for storing massive amount of exercise names
    :return: list of exercise names"""
    return ['Neck Flexion', 'Lateral Neck Flexion', 'Wall Front Neck Bridge',
       'Wall Side Neck Bridge', 'Neck Extension', 'Seated Neck Extension',
       'Seated Neck Extension:  Harness', 'Neck Retraction',
       'Wall Rear Neck Bridge', 'Lying Neck Retraction', 'Front Raise',
       'Military Press', 'Military Press:  Seated'
       'Front Raise:  Alternating', 'Front Raise:  One Arm',
       'Shoulder Press', 'Shoulder Press:  Seated', 'Arnold Press',
       'Shoulder Press:  One Arm', 'Reclined Shoulder Press',
       'Shoulder Press:  Parallel Grip', 'Pike Press (between benches)',
       'Pike Press (between benches):  Elevated (between benches)',
       'Upright Row', 'Lateral Raise', 'Lateral Raise:  One Arm',
       'Upright Row:  One Arm', 'Upright Row:  with rope', 'Y Raise',
       'Incline Lateral Raise', 'Lateral Raise:  other machine',
       'Rear Delt Row', 'Reverse Fly',
       'Rear Delt Row:  Standing Rear Delt Row (stirrups)',
       'Rear Lateral Raise', 'Seated Rear Lateral Raise',
       'Lying Rear Lateral Raise', 'Seated Rear Delt Row',
       'Seated Rear Delt Row:  alternative machine', 'Seated Reverse Fly',
       'Seated Reverse Fly:  pronated grip',
       'Rear Delt Inverted Row (high bar)',
       'Rear Delt Inverted Row (on hips)', 'Front Lateral Raise',
       'Full Can Lateral Raise', 'Lying Lateral Raise', 'Triceps Dip',
       'Triceps Dip:  kneeling', 'Close Grip Bench Press',
       'Lying Triceps Extension',
       'Lying Triceps Extension:  Skull Crusher', 'Triceps Extension',
       'Bent-over Triceps Extension', 'Pushdown', 'Pushdown:  One Arm',
       'Pushdown:  with back support', 'Pushdown:  with V-bar attachment',
       'Triceps Extension:  with rope', 'Kickback',
       'One Arm Triceps Extension (on bench)',
       'Triceps Dip:  alternative machine',
       'Triceps Extension:  with preacher pad New!',
       'Standing Triceps Dip', 'Bench Dip', 'Bench Dip:  heel on floor',
       'Close Grip Push-up', 'Close Grip Push-up:  on knees',
       'Close Grip Push-up:  Incline on bar', 'Curl', 'Alternating Curl',
       'Curl:  with stirrups', 'Curl:  One Arm Curl', 'Incline Curl',
       'Inverted Biceps Row', 'Preacher Curl', 'Prone Incline Curl',
       'Concentration Curl', 'Preacher Curl: Stirrups',
       'Preacher Curl: arms high', 'Arm Curl', 'Reverse Curl',
       'Hammer Curl', 'Wrist Curl', 'Grip', 'One Hand Grip', 'One Hand',
       'Reverse Wrist Curl', 'Seated Pronation ', 'Seated Supination',
       'Bent-over Row', 'Bent-over Row:  Underhand',
       'One Arm Bent-over Row', 'One Arm Straight Back Seated High Row',
       'Seated Row', 'Seated Row:  Straight Back', 'Seated Wide Grip Row',
       'Seated Wide Grip Row:  Straight Back', 'Lying Row', 'Incline Row',
       'Incline Row:  Close Grip', 'Seated Rows',
       'Seated Rows:  Narrow Grip', 'Seated Rows:  Wide GripLow Bar',
       'Seated Rows (Others)', 'Seated Rows (Others):  Seated Low Row',
       'Seated Rows (Others):  Seated High Row', 'T-bar Row',
       'T-bar Row:  Close grip', 'Seated Row:  Wide Grip',
       'Seated Row (no chest pad)',
       'Seated Row (no chest pad):  Straight Back',
       'Underhand Seated Row', 'Inverted Row',
       'Inverted Row:  Feet Elevated', 'Inverted Row:  High Bar',
       'Inverted Row:  On Hips', 'Inverted Row:  One Arm', 'Row',
       'Row:  One Arm', 'Pull-up (open-centered bar)',
       'Pull-up (open-centered bar):  Standing',
       'Parallel Close Grip Pull-up', 'Pullover', 'Bent-over Pullover',
       'Close Grip Pulldown', 'Pulldown',
       'Pulldown:  Parallel Grip Pulldown', 'Pullup/Chinup',
       'Pullup/Chinup:  Chinup',
       'Pullup/Chinup:  Parallel Close Grip Pull-up',
       'Pullup/Chinup:  Parallel Grip Pull-up', 'Pullup/Chinup:  Pull-up',
       'Underhand Pulldown', 'Front Pulldown', 'Chin-up', 'Pull-up',
       'Archer Pull-up', 'Pull-up:  Parallel Grip',
       'One Arm Pull-up\xa0New!', 'Pull-up:  Self-assisted', 'Shrug',
       'Trap Bar Shrug', 'Shrug with Stirrups', 'Seated Shrug',
       'Gripless Shrug', 'Inverted Shrug',
       'Seated Shoulder External Rotation',
       'Seated Shoulder External Rotation:  Standing',
       'Lying Shoulder External Rotation',
       'Upright Shoulder External Rotation (with support)',
       'Shoulder External Rotation',
       'Standing Shoulder Internal Rotation',
       'Shoulder Internal Rotation',
       'Shoulder Internal Rotation:  on floor', 'Chest Dip',
       'Chest Dip:  kneeling', 'Bench Press', 'Bench Press:  Power Lift',
       'Decline Bench Press', 'Flies', 'Flies:  Lying Fly',
       'Flies:  Seated Fly', 'Flies:  Standing Fly', 'Presses',
       'Presses:  Bench Press', 'Presses:  Chest PressStanding',
       'Presses:  Decline Chest Press', 'Fly', 'Chest Press',
       'Decline Chest Press', 'Flies:  Pec Deck Fly',
       'Presses:  Chest Pressalternative machine', 'Standing Chest Dip',
       'Push-up', 'Push-up:  Archer', 'Push-up:  Incline',
       'Push-up:  on knees', 'Clap Push-up', 'Depth Push-up',
       'Incline Bench Press', 'Incline Chest Press', 'Incline Fly',
       'Incline Chest Press:  on Military Press Machine',
       'Decline Push-up', 'Decline Push-up:  on stability ball',
       'Chest Dip ', 'Standing Fly ', 'Incline Shoulder Raise',
       'Push-up Plus', 'Bent Knee Good-morning', 'Deadlifts',
       'Deadlifts:  Stiff-leg DeadliftStraight-back', 'Hip Thrust',
       'Lunge', 'Lunge:  Rear Lunge', 'Single Leg Split Squat',
       'Single Leg Split Squat:  Single Leg Squat',
       'Single Leg Split Squat:  Split Squat', 'Squat',
       'Squat:  Front Squat', 'Squat:  Full Squat',
       'Squat:  Safety Squat', 'Step-up', 'Glute Kickback', 'Rear Lunge',
       'Split Squat', 'Split Squat:  Two Arms', 'Standing Hip Extension',
       'Standing Hip Extension:  Bent-over', 'Stiff-leg Deadlift',
       'Stiff-leg Deadlift:  Straight-back', 'Step-up:  Step Down',
       'Deadlift', 'Deadlift:  Stiff-leg DeadliftStraight-back',
       'Leg Presses', 'Leg Presses:  45° Leg Press',
       'Leg Presses:  Lying Leg Press', 'Leg Presses:  Seated Leg Press',
       'Lying Hip Extension', 'Reverse Hyper-extension', 'Hip Extensions',
       'Hip Extensions:  Bent-over', 'Hip Extensions:  Lying',
       'Hip Extensions:  Standingalternative machine',
       'Glute Kickback:  Bent-over', 'Glute Kickback:  Kneeling',
       'Glute Kickback:  Standing', 'Squat:  V-Squat',
       'Squat:  Hack Squat', 'Single Leg Squat',
       'Split Squat:  Single Leg Split Squat',
       'Single Leg Stiff Leg Deadlift', 'Single Leg Squat (leg wrapped)',
       'Step Down', 'Hip Bridge', 'Hip Abduction',
       'Seated Hip Internal Rotation', 'Lying Hip Abduction',
       'Seated Hip Abduction', 'Standing Hip Abduction', 'Twist',
       'Side Bend', 'Assisted Wheel Rollout', 'Lying Leg Raise',
       'Lying Leg Raise:  on bench', 'Lying Leg Raise:  Straight Leg',
       'Standing Leg Raise', 'Standing Leg Raise:  Straight Leg',
       'Hip Flexion', 'Vertical Leg Raise', 'Decline Sit-up',
       'Hanging Leg Raise', 'Hanging Leg Raise:  Straight Leg',
       'Incline Leg Raise', 'Incline Leg Raise:  arms on pads',
       'Incline Straight Leg Raise',
       'Incline Straight Leg Raise:  arms on pads', 'Roman Chair Sit-up',
       'Seated Leg Raise', 'Vertical Leg Raise:  on Parallel Bars',
       'Vertical Leg Raise:  Straight Leg', 'Leg Raises',
       'Leg Raises:  Hanging Leg Raisewith ab strapsStraight Leg',
       'Leg Raises:  Incline Leg Raisearms on pads',
       'Leg Raises:  Incline Straight Leg Raisearms on pads',
       'Leg Raises:  Lying Leg RaiseAlternatingon floor',
       'Leg Raises:  Lying Straight Leg RaiseAlternating',
       'Leg Raises:  Seated Leg Raise',
       'Leg Raises:  Vertical Leg Raiseon parallel barsStraight Leg',
       'Jack-knife on Ball', 'Scissor Kick', 'Wheel',
       'Wheel:  Jack-Knife', 'Wheel:  Rollout', 'Wheel:  Pike', 'Discs',
       'Discs:  Pike', 'Mountain Climber', 'Pike',
       'Single Leg Split Squat:  Side Split Squat',
       'Squat:  Trap Bar Squat', 'Single Leg Squat (plate loaded)',
       'Squat:  Barbell Machine', 'Leg Extension', 'V-Squat',
       'Single Leg Squat:  Box', 'Step-up:  Step-down', 'Glute-Ham Raise',
       'Good-morning', 'Hyperextension', 'Hyperextension (45°)',
       'Straight-leg Deadlift', 'Straight-leg Deadlift:  Straight-back',
       'Lying Leg Curl', 'Standing Leg Curl',
       'Straight-back Straight-leg Deadlift', 'Kneeling Leg Curl',
       'Seated Leg Curl', 'Bent-over Leg Curl', 'Hamstring Raise',
       'Glute-Ham Raise:  hands behind hips',
       'Single Leg Hanging Hamstring Bridge',
       'Single Leg 45° Hyperextension', 'Straight Hip Leg Curl (on ball)',
       'Inverse Leg Curl', 'Leg Curl', 'Hanging Leg Curl',
       'Straight Hip Leg Curl', 'Hip Adduction', 'Seated Hip Adduction',
       'Standing Hip Adduction', 'Lying Hip Adduction',
       'Standing Calf Raise',
       'Standing Calf Raise:  One Arm Single Leg Calf Raise',
       'Standing Calf Raise:  Single Leg', '45° Calf Press',
       'Calf Extension', 'Seated Calf Press', '45° Calf Raise',
       'Donkey Calf Raise', 'Lying Calf Press', 'Single Leg Calf Raise',
       'Forward Angled Single Leg Calf Raise',
       'Safety Barbell Seated Calf Raise', 'Seated Calf Raise',
       'Safety Bar Reverse Calf Raise', 'Reverse Calf Raise',
       'Reverse Calf Raise:  Single Leg', '45° Reverse Calf Press',
       '45° Reverse Calf Raise', 'Reverse Calf Extension',
       '45° Reverse Calf Raise (plate loaded)',
       '45° Reverse Calf Raise (on hack press)',
       'Hack Reverse Calf Raise', 'Lying Reverse Calf Press',
       'Seated Reverse Calf Press']
