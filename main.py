# Authors: Samuel Franco and Dekang Lu
# Description: main execute
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from interface import GUI

if __name__ == "__main__":
    root = ttk.Window(themename="solar")
    app = GUI(root)
    root.mainloop()
