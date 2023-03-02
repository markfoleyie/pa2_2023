import tkinter as tk
from tkinter import ttk


class MyGUI:
    def __init__(self, parent):
        self.parent = parent
        self.frame1 = ttk.Frame(self.parent)
        self.frame1.grid()
        self.label1 = ttk.Label(self.frame1, text="Starting...")
        self.label1.grid(row=0, column=0)
        self.label1.bind("<Enter>", lambda e: self.label1.configure(text="Moved mouse inside"))
        self.label1.bind("<Leave>", lambda e: self.label1.configure(text="Moved mouse outside"))
        self.label1.bind('<B3-Motion>', lambda e: self.label1.configure(text='right button drag to %d,%d' % (e.x, e.y)))
        self.button1 = ttk.Button(self.frame1, text="Print Stuff",
                                  command=lambda a="I hit the button": self.print_handler(a))
        self.button1.grid(row=0, column=1)
        self.button2 = ttk.Button(self.frame1, text="Print More Stuff",
                                  command=lambda a="I hit the other button": self.print_handler(a))
        self.button2.grid(row=0, column=2)
        self.button1 = ttk.Button(self.frame1, text="Print Stuff",
                                  command=self.print_handler)
        self.button1.grid(row=1, column=1)

        self.choice = tk.StringVar()
        self.label2 = ttk.Label(self.frame1, textvariable=self.choice)
        self.label2.grid(row=3, column=0, columnspan=3)

        self.radio1 = tk.Radiobutton(self.frame1, text="Fahrenheit to Celsius", variable=self.choice, value='1')
        self.radio2 = tk.Radiobutton(self.frame1, text="Celsius to Fahrenheit", variable=self.choice, value='2')
        self.radio1.grid(row=1, column=0, columnspan=3)
        self.radio2.grid(row=2, column=0, columnspan=3)

    def print_handler(self, random_stuff="qwerty"):
        print_stuff(f"random junk: {random_stuff}")


def print_stuff(stuff):
    print(f"This prints:\n{stuff}")


def main():
    root = tk.Tk()
    MyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
