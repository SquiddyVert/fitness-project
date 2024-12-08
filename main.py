#authors: Samuel Franco & Dekang Lu
import tkinter
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from workout2 import Workout
from functions import workoutNames
from profile_1 import Profile
from interface import GUI

def main():
    print("hello")



if __name__ == "__main__":
    root = ttk.Window(themename="solar")
    app = GUI(root)
    root.mainloop()
