import tkinter as tk
from tkinter import ttk


class MyGUI:
    def __init__(self, parent):
        self._parent = parent
        self._frame1 = ttk.Frame(self._parent)
        self._frame1.grid()
        self._button1 = ttk.Button(self._frame1, text="Hello World")
        self._button1.grid(row=0, column=0)


if __name__ == '__main__':
    root = tk.Tk()
    MyGUI(root)
    root.mainloop()
