import tkinter as tk
from tkinter import filedialog


class MyGUI:
    def __init__(self, my_parent):
        self.my_parent = my_parent

        self.my_parent.title("text file viewer")

        self.frame1 = tk.Frame(self.my_parent)
        self.frame1.pack()

        self.btn = tk.Button(self.frame1, text="testing")
        self.btn.pack()

        self.menu = tk.Menu(self.my_parent)

        self.file_menu = tk.Menu(self.menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit_gui)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.my_parent.config(menu=self.menu)

    def open_file(self):
        pass

    def quit_gui(self):
        pass


def main():
    root = tk.Tk()
    MyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
