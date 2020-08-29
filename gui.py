#!/usr/bin/python3

import tkinter as tk

def handle_click(event):
    print("The button was clicked!")

def main(): 
    print("PiPy Cam ... starting up ...")

    # for testing
    # tk._test()

    window = tk.Tk()

    greeting = tk.Label(text="Hello")
    greeting.pack()

    button = tk.Button(
            text = "Click Me",
            width = 25,
            height = 5,
            bg = "blue",
            fg = "yellow",
            )
    button.bind("<Button-1>", handle_click)
    button.pack()


    window.mainloop()

if __name__ == "__main__":
    main()
