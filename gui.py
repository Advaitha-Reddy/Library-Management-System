import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk
from logic import register_member, add_book, delete_book, issue_book, return_book

class LibraryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("School Library Management System")
        self.root.state('zoomed')  # Maximize window
        self.root.minsize(600, 600)

        # Load background image
        try:
            self.original_image = Image.open("library.png")
        except Exception as e:
            print("Image load failed:", e)
            self.original_image = None

        # Canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Welcome label
        self.welcome_label = tk.Label(
            self.root,
            text="Welcome to School Library System",
            font=("Lucida Handwriting", 28, "bold italic"),
            bg="#333333",
            fg="white",
            padx=20,
            pady=10
        )
        self.welcome_label.place(relx=0.5, rely=0.1, anchor="center")

        # Buttons
        self.buttons_info = [
            ("Register Member", self.open_register_member),
            ("Add Book", self.open_add_book),
            ("Delete Book", self.open_delete_book),
            ("Issue Book", self.open_issue_book),
            ("Return Book", self.open_return_book)
        ]
        for i, (text, cmd) in enumerate(self.buttons_info):
            btn = tk.Button(
                self.root,
                text=text,
                width=20,
                height=2,
                command=cmd,
                bg="#0052cc",
                fg="white",
                font=("Helvetica", 14, "bold"),
                relief="raised"
            )
            btn.place(relx=0.5, rely=0.3 + i*0.1, anchor="center")

        self.root.bind("<Configure>", self.on_resize)
        self.bg_img = None
        self.root.after(100, self.update_background)  # Delay for initial load

    def update_background(self):
        if not self.original_image:
            return

        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 100 or h < 100:
            return

        img_ratio = self.original_image.width / self.original_image.height
        canvas_ratio = w / h

        if canvas_ratio > img_ratio:
            new_width = w
            new_height = int(w / img_ratio)
        else:
            new_height = h
            new_width = int(h * img_ratio)

        resized_img = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized_img)

        self.canvas.delete("all")
        self.canvas.create_image(w // 2, h // 2, image=self.bg_img, anchor="center", tags="bg_img")

    def on_resize(self, event):
        if event.widget == self.root:
            self.update_background()

    # === BUTTON FUNCTIONALITIES ===

    def open_register_member(self):
        self.open_form_window(
            "Register Member",
            [("Roll No", "roll"), ("Name", "name")],  # param names must match function
            register_member
        )

    def open_add_book(self):
        self.open_form_window(
            "Add Book",
            [("Title", "title"), ("Author", "author"), ("Number of Copies", "copies")],
            add_book
        )

    def open_delete_book(self):
        self.open_form_window(
            "Delete Book",
            [("Book ID", "book_id")],
            delete_book
        )

    def open_issue_book(self):
        self.open_form_window(
            "Issue Book",
            [("Roll No", "roll"), ("Book ID", "book_id")],
            issue_book
        )

    def open_return_book(self):
        self.open_form_window(
            "Return Book",
            [("Roll No", "roll"), ("Book ID", "book_id")],
            return_book
        )

    def open_form_window(self, title, fields, action_func):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x300")
        self.center_window(popup)

        entries = {}

        for i, (label_text, var_name) in enumerate(fields):
            label = tk.Label(popup, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entry = tk.Entry(popup, width=30)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[var_name] = entry

        def submit():
            inputs = {k: e.get().strip() for k, e in entries.items()}

            # Validate numbers
            for num_field in ['copies', 'book_id', 'roll']:
                if num_field in inputs:
                    if not inputs[num_field].isdigit():
                        messagebox.showerror("Invalid Input", f"{num_field.capitalize()} must be a number.")
                        return
                    inputs[num_field] = int(inputs[num_field])  # convert to int

            try:
                result = action_func(**inputs)
                #messagebox.showinfo("Success", "Operation completed successfully!")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        submit_btn = tk.Button(popup, text="Submit", command=submit)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def center_window(self, win, width=400, height=300):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LibraryApp()
    app.run()
