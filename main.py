import os
import sys
import tkinter as tk
from LogGenerator import LogGenerator

def main():
    logGenerator = tk.Tk()
    LogGenerator(logGenerator)
    logGenerator.mainloop()

if __name__ == "__main__":
    main()