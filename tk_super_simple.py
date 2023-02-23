"""
Tkinter generic tasks

1. LOOK: Define the look of the screen
2. DO; Define the event handler routines
3. LOOK associated with DO: Associate interesting keyboard events with their handlers.
4. LISTEN: Loop forever, observing events. Exit when an exit event occurs.

"""

import tkinter as tk
from tkinter import ttk, messagebox

GUI_TITLE = "Tk in-class demo"


class MyGUI:
    def __init__(self, parent):
        # Basic workflow:
        # 1. Create a GUI object and associate it with its parent
        # 2. Pack it or place it on grid - set up a 'geometry manager'

        # Remember who the parent window is
        self._parent = parent

        self._parent.title(GUI_TITLE)

        # Make protocol handler to manage interaction between the application and the window handler
        self._parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Create a container to hold the widgets
        self._padding = {'padx': 5, 'pady': 5, 'sticky': tk.W}

        self._frame1 = ttk.Frame(self._parent)
        self._frame1.grid(row=0, column=0, **self._padding)

        self._label1 = ttk.Label(self._frame1, text="Placeholder text...")
        self._label1.grid(row=0, column=0, **self._padding)

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self._parent.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    MyGUI(root)
    root.mainloop()
