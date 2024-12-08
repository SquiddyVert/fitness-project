# Authors: Samuel Franco and Dekang Lu
import tkinter
from tkinter import ttk
from tkinter import messagebox
from profile_1 import Profile
from interface import GUI
from workout import Workout

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
    #creates a variable for whatever name is currently in the text box
    updatedcurrentProfile = GUI.currentProfileEntry.get()

    # Check if the profile exists in the profiles dictionary, if so updates the currentprofile label and variable accordingly
    if updatedcurrentProfile in GUI.profiles:
        GUI.currentProfile = updatedcurrentProfile 
        GUI.currentuserprofileLabel.config(text=f"{GUI.currentProfile}")
    else:
        tkinter.messagebox.showinfo("Error", "Profile not found! Check 'output profiles' to see what profiles are availableto choose from")

def add_excercise_row(GUI):
    """Add a new row for excercise name"""
    # Create a frame for the row
    excercise_frame = tkinter.Frame(GUI.dynamic_frame, bd=2, relief='groove')
    excercise_frame.pack(fill='x', pady=5)

    nameLabel = tkinter.Label(excercise_frame,text="Excercise name")
    nameLabel.pack(side='left', padx=5)

    # Create a dropdown (Combobox)
    dropdown_var = tkinter.StringVar()
    dropdown = ttk.Combobox(excercise_frame, textvariable=dropdown_var, width=20, state="normal")
    dropdown.pack(side='left', padx=5)
    dropdown['values'] = GUI.dropdown_options  

    def on_dropdown_type(*args):
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

    add_set_button = tkinter.Button(excercise_frame, text="Add Set", command=lambda: add_set_row(GUI,excercise_frame))
    add_set_button.pack(side='left', padx=5)

    delete_excercise_button = tkinter.Button(
        excercise_frame,
        text="Delete Excercise",
        command=lambda: delete_workout_row(GUI, excercise_frame)
    )
    delete_excercise_button.pack(side='left', padx=5)
    GUI.excercises.append({"frame": excercise_frame, "name": dropdown_var, "sets": []})

def add_set_row(GUI, excercise_frame):
    """Add a new row for a new sets with reps and weights."""
    for excercise in GUI.excercises:
        if excercise["frame"] == excercise_frame:
            set_frame = tkinter.Frame(excercise_frame)
            set_frame.pack(fill='x', padx=20, pady=2)

            repLabel = tkinter.Label(set_frame,text="reps")
            repLabel.pack(side='left', padx=5)
            rep_var = tkinter.IntVar()
            reps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            repscb = ttk.Combobox(set_frame, values=reps)
            repscb.pack(side='left', padx=5)

            def update_reps_var(event):
                try:
                    rep_var.set(int(repscb.get()))
                except ValueError:
                    rep_var.set(0)

            repscb.bind("<<ComboboxSelected>>", update_reps_var)
    
            weightLabel = tkinter.Label(set_frame,text="weights(0  none)")
            weightLabel.pack(side='left', padx=5)
            weight_var = tkinter.DoubleVar()
            weights = [0, 5, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0]
            weightcb = ttk.Combobox(set_frame, values=weights)
            weightcb.pack(side='left', padx=5)

            def update_weight_var(event):
                try:
                    weight_var.set(float(weightcb.get()))
                except ValueError:
                    weight_var.set(0.0)
    
            weightcb.bind("<<ComboboxSelected>>", update_weight_var)
    
            delete_set_button = tkinter.Button(
                set_frame,
                text="Delete Set",
                command=lambda: delete_set_row(GUI,excercise, set_frame)
            )
            delete_set_button.pack(side='left', padx=5)
            excercise["sets"].append({"frame": set_frame, "rep": rep_var, "weight": weight_var})
            break

def delete_workout_row(GUI, excercise_frame):
    """Delete a workout row and all its associated sets."""
    for excercise in GUI.excercises:
        if excercise["frame"] == excercise_frame:
            # Remove all set frames
            for set_frame in excercise["sets"]:
                set_frame.destroy()

            # Remove the workout frame
            excercise_frame.destroy()

            # Remove from tracking list
            GUI.excercises.remove(excercise)
            break

def delete_set_row(GUI, excercise, set_frame):
    """Delete a specific set row."""
    # Remove the set frame from the workout's tracking list
    if set_frame in excercise["sets"]:
        excercise["sets"].remove(set_frame)

    # Destroy the set frame
    set_frame.destroy()

def reset_log_tab(GUI):
        """Clear the Log Tab and reset it to its initial state."""
        # Destroy all widgets in the dynamic frame
        for widget in GUI.dynamic_frame.winfo_children():
            widget.destroy()

        # Clear the excercise tracker list
        GUI.excercises.clear()
    
def save_data(GUI):
    """Save the current workouts and sets to the data list and display them in the table."""
    GUI.data.clear()  # Clear previous data
    for excercise in GUI.excercises:
        excercise_name = excercise["name"].get()
        for set_data in excercise["sets"]:
            rep = set_data["rep"].get()
            weight = set_data["weight"].get()
            GUI.data.append((excercise_name, rep, weight))

    # Update the table in the Table tab
    for row in GUI.tree.get_children():
        GUI.tree.delete(row)
    for excercise_name, rep, weight in GUI.data:
        GUI.tree.insert("", "end", values=(excercise_name, rep, weight))
    
    GUI.reset_log_tab()
    GUI.my_notebook.select(3)


def excerciseNames():
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
