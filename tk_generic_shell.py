"""
Generic shell program to illustrate GUI programming with Tkinter

This will...

Mark Foley
March 2021
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


class MyGUI:
    """
    All of the GUI stuff lives here
    """

    def __init__(self, parent):
        """
        All of the GUI 'look' lives here.
        """
        self._parent = parent

        self._parent.title("This text displays in the title bar")
        self._parent.geometry("600x600")

        # Make protocol handler to manage interaction between the application and the window handler
        self._parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self._padding = {'padx': 5, 'pady': 5, 'sticky': tk.W}

        self._frame1 = ttk.Frame(self._parent)
        self._frame1.grid(row=0, column=0, **self._padding)

        self._label1 = tk.Label(self._frame1, text="Label text", )
        self._label1.grid(row=0, column=0, **self._padding)

        # set up menu
        self._menu = tk.Menu(self._parent)

        self._file_menu = tk.Menu(self._menu)
        self._file_menu.add_command(label="Open", command=self.open_file)
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Exit", command=self.catch_destroy)

        self._menu.add_cascade(label="File", menu=self._file_menu)

        self._parent.config(menu=self._menu)

        self._chosen_file = tk.StringVar()

        self._frame2 = ttk.Frame(self._parent, padding=5, borderwidth=2, relief="sunken", height=50, width=50)
        self._frame2.grid(row=1, column=0, **self._padding)
        self._file_label = ttk.Label(self._frame2)
        self._file_label.grid(column=0, row=0, **self._padding)

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self._parent.destroy()

    def open_file(self):
        # Can run file dialogue from anywhere
        chosen_file = filedialog.askopenfilename(filetypes=(("Python files", "*.py"),
                                                            ("Text files", "*.txt"),
                                                            ("Markdown files", "*.md;*.mkd"),
                                                            ("All files", "*.*")))
        self._chosen_file.set(chosen_file)
        self._file_label["text"] = self._chosen_file.get()

        # print("You pressed File->Open\n{}".format(chosen_file))


def main():
    root = tk.Tk()

    root.withdraw()
    my_file = filedialog.askopenfilename()
    messagebox.showinfo("Title text", f"You chose {my_file}")
    # Show window again
    root.deiconify()

    MyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
