"""
Tkinter generic tasks

1. LOOK: Define the look of the screen
2. DO; Define the event handler routines
3. LOOK associated with DO: Associate interesting keyboard events with their handlers.
4. LISTEN: Loop forever, observing events. Exit when an exit event occurs.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class GUI:
    """
    Class that defines the GUI. This approach helps partition GUI-related elements
    from other parts of the program. Also avoids the use of global variables later.
    Ultimately reduces complexity.
    """

    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Temperature Converter")

        self.parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.main_frame = tk.Frame(self.parent, padx=20, pady=20)
        self.main_frame.grid(row=0, column=0)

        self.choice = tk.IntVar()
        self.result = tk.StringVar()

        self.radio1 = tk.Radiobutton(self.main_frame, text="Fahrenheit to Celsius", variable=self.choice, value=1)
        self.radio2 = tk.Radiobutton(self.main_frame, text="Celsius to Fahrenheit", variable=self.choice, value=2)
        self.radio1.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.radio2.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        self.enter_label = tk.Label(self.main_frame, padx=5, pady=5, text="Enter Value")
        self.enter_label.grid(row=2, column=0, sticky=tk.W)

        self.enter_box = tk.Entry(self.main_frame)
        self.enter_box.grid(row=2, column=1, sticky=tk.W)

        self.btn = tk.Button(self.main_frame, text="Convert", command=self.calculate_result, padx=5, pady=5, bg="red",
                             fg="white")
        self.btn.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)

        self.result_frame = tk.Frame(self.main_frame, padx=10, pady=10, borderwidth=2, relief=tk.SUNKEN)
        self.result_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.result_label = tk.Label(self.result_frame, padx=5, pady=5, text="Result:")
        self.result_label.grid(row=0, column=0, sticky=tk.W)

        self.result_box = tk.Label(self.result_frame, textvariable=self.result)
        self.result_box.grid(row=0, column=1, sticky=tk.W)

    def calculate_result(self):
        self.result.set(do_non_gui_stuff(self.choice.get(), self.enter_box.get()))

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()


def do_non_gui_stuff(choice, value):
    """
    Formulae
    f -> c = (Tf -32) / 1.8
    c -> f = (Tc * 1.8) +32
    """
    try:
        if choice == 1:
            # f -> c
            res = (float(value) - 32) / 1.8
            return "{} F = {} C".format(float(value), res)
        elif choice == 2:
            # c -> f
            res = (float(value) * 1.8) + 32
            return "{} C = {} F".format(float(value), res)
        else:
            raise ValueError("You must choose conversion type.")
    except Exception as e:
        return "Problem!", "{}".format(e)


if __name__ == "__main__":
    root = tk.Tk()
    GUI(root)
    root.mainloop()
