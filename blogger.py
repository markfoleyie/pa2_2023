import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import font

HOST = "http://localhost:5000/"
URLS = {
    "posts": "list-posts/",
    "categories": "list-categories/",
    "users": "list-users/",
    "post": "post/",
    "register": "register/",
}


class MyGUI:
    def __init__(self, root, gui_settings):

        self.root = root

        for k, v in gui_settings.items():
            setattr(self, k, v)

        # self.root.geometry(f"{self.width}x{self.height}")
        # self.root.resizable(self.resizable_width, self.resizable_height)

        # Make protocol handler to manage interaction between the application and the window handler
        self.root.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.padding = {
            'padx': 5,
            'pady': 5,
            'ipadx': 5,
            'ipady': 5,
        }

        # Set up fonts for text area
        arial_bold = font.Font(family="Arial", size=14, weight=font.BOLD)
        arial_normal = font.Font(family="Arial", size=14, weight=font.NORMAL)
        arial_italic = font.Font(family="Arial", size=14, slant=font.ITALIC)

        self.users = None
        self.display_users = []
        self.selected_user = tk.StringVar()
        self.user_token = None
        self.categories = None
        self.display_categories = []
        self.selected_category = tk.StringVar()
        self.selected_category_id = None
        self.all_posts = None

        self.populate_users()
        self.populate_categories()

        self.root.title("Blogger")
        self.frame1 = ttk.Frame(self.root)
        self.frame1.grid(**self.padding)
        self.main_label = ttk.Label(self.frame1, text="Posts", font=("Arial", 20), )
        self.main_label.grid(row=0, column=0, **self.padding, sticky="w")
        self.users_combo = ttk.OptionMenu(self.frame1, self.selected_user, *self.display_users, command=self.get_user)
        self.users_combo.grid(row=0, column=1, **self.padding, sticky="w")
        self.posts = ScrolledText(self.frame1, wrap=tk.WORD)
        self.posts.tag_configure("bo", font=arial_bold)
        self.posts.tag_configure("no", font=arial_normal)
        self.posts.tag_configure("it", font=arial_italic)
        self.posts.grid(row=1, column=0, columnspan=2, sticky="nwse")
        self.new_post = ScrolledText(self.frame1, wrap=tk.WORD, width=85, height=3)
        self.new_post.grid(row=2, column=0, rowspan=2, **self.padding, sticky="nws")
        self.post_submit = tk.Button(self.frame1, text="Post", bg="green", fg="white", command=self.submit_post)
        self.post_submit.grid(row=3, column=1, **self.padding, sticky="e")
        self.categories_combo = ttk.OptionMenu(self.frame1, self.selected_category, *self.display_categories,
                                               command=self.get_category)
        self.categories_combo.grid(row=2, column=1, **self.padding, sticky="e")

        self.populate_posts_list()

    def submit_post(self):
        contents = self.new_post.get("1.0", tk.END)
        if contents:
            first_break = contents.find("\n")
            if first_break == -1:
                first_break = 0
            submit_post({
                "owner_token": self.user_token,
                "category_id": self.selected_category_id,
                "title": contents[0:first_break].strip(),
                "content": contents[first_break:].strip()
            })

            self.populate_posts_list()
            self.new_post.delete("1.0", tk.END)

    def populate_posts_list(self):
        data = self.all_posts = get_posts()
        self.posts.delete("1.0", tk.END)
        if data["posts"]:
            for item in data["posts"]:
                self.posts.insert(tk.END, f"\n{item['title']}", "bo")
                self.posts.insert(tk.END, f"\n{item['content']}", "no")
                self.posts.insert(tk.END, f"\n{item['category']} ... {item['owner']} ... {item['created']}\n", "it")

    def populate_users(self):
        self.display_users = ["", ]
        data = self.users = get_users()
        if data["users"]:
            for user in data["users"]:
                self.display_users.append(user["email"])
        else:
            pass

    def populate_categories(self):
        self.display_categories = ["", ]
        data = self.categories = get_categories()
        if data["categories"]:
            for item in data["categories"]:
                self.display_categories.append(item["name"])
        else:
            pass

    def get_user(self, *args):
        user_email = self.selected_user.get()
        for user in self.users["users"]:
            if user["email"] == user_email:
                self.user_token = user["token"] or None

    def get_category(self, *args):
        category = self.selected_category.get()
        for cat in self.categories["categories"]:
            if cat["name"] == category:
                self.selected_category_id = cat["id"] or None

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()


def submit_post(post):
    try:
        headers = {'Authorization': post['owner_token']}
        response = requests.post(f"{HOST}{URLS['post']}", headers=headers, json=post)

        if response.status_code < 200 or response.status_code > 299:
            raise ValueError(f"invalid status code: {response.status_code}")

        if not response.json():
            return None

        return response.json()

    except Exception as e:
        print(f"{e}")
        return None


def get_posts():
    try:
        response = requests.get(f"{HOST}{URLS['posts']}")

        if response.status_code < 200 or response.status_code > 299:
            raise ValueError(f"invalid status code: {response.status_code}")

        if not response.json():
            return None

        return response.json()

    except Exception as e:
        print(f"{e}")
        return None


def get_users():
    try:
        response = requests.get(f"{HOST}{URLS['users']}")

        if response.status_code < 200 or response.status_code > 299:
            raise ValueError(f"invalid status code: {response.status_code}")

        if not response.json():
            return None

        return response.json()

    except Exception as e:
        print(f"{e}")
        return None


def get_categories():
    try:
        response = requests.get(f"{HOST}{URLS['categories']}")

        if response.status_code < 200 or response.status_code > 299:
            raise ValueError(f"invalid status code: {response.status_code}")

        if not response.json():
            return None

        return response.json()

    except Exception as e:
        print(f"{e}")
        return None


def main():
    GUI_SETTINGS = {
        # "width": 800,
        # "height": 600,
        # "status_bar_height": 10,
        # "resizable_width": False,
        # "resizable_height": False,
        # "title_text": "Tk Demo - Various Widgets",
    }

    root = tk.Tk()
    MyGUI(root, GUI_SETTINGS)
    root.mainloop()


if __name__ == "__main__":
    main()
