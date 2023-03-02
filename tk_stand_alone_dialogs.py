"""
This is an example of using Tkinter to create stand-alone dialogs.

Tkinter has many such dialogs for messaging, file opening/saving, colour picking and so on.
You can also create your own.

We create a root window in the usual way and then hide (withdraw) it.
Then we deal with any modal dialogs
Finally, we destroy the window.

Mark Foley
March 2021.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


def get_file_contents(file):
    try:
        with open(file, "r") as fh:
            content = fh.read()
        return content
    except Exception as e:
        return f"{e}"


def main():
    root = tk.Tk()

    root.withdraw()
    my_file = filedialog.askopenfilename(filetypes=(("Python files", "*.py"),
                                                    ("Text files", "*.txt"),
                                                    ("Markdown files", "*.md;*.mkd"),
                                                    ))

    messagebox.showinfo(f"You chose {my_file}", get_file_contents(my_file))

    messagebox.showinfo(f"Docstring for {__file__}", f"{__doc__}")
    root.destroy()
    # Show window again
    # root.deiconify()
    print("Finished.")


if __name__ == "__main__":
    main()
