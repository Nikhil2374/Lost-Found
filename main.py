import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

class LostAndFoundApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Lost and Found")
        self.master.geometry("700x600")
        self.master.configure(bg="#e8f4f8")

        self.items = []
        self.selected_image_path = None

        # Title Label
        self.title_label = tk.Label(master, text="Lost and Found", font=("Helvetica", 24, "bold"), bg="#e8f4f8", fg="#333")
        self.title_label.pack(pady=20)

        # Input Frame
        self.input_frame = tk.Frame(master, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.input_frame.pack(pady=10, padx=20, fill=tk.X)

        # Input Labels and Entries
        self.item_label = tk.Label(self.input_frame, text="Item:", bg="#ffffff")
        self.item_label.grid(row=0, column=0, padx=10, pady=10)

        self.item_entry = tk.Entry(self.input_frame, width=25, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
        self.item_entry.grid(row=0, column=1, padx=10, pady=10)

        self.description_label = tk.Label(self.input_frame, text="Description:", bg="#ffffff")
        self.description_label.grid(row=1, column=0, padx=10, pady=10)

        self.description_entry = tk.Text(self.input_frame, width=50, height=5, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)

        self.contact_label = tk.Label(self.input_frame, text="Contact Info:", bg="#ffffff")
        self.contact_label.grid(row=2, column=0, padx=10, pady=10)

        self.contact_entry = tk.Entry(self.input_frame, width=25, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
        self.contact_entry.grid(row=2, column=1, padx=10, pady=10)

        self.found_var = tk.BooleanVar()
        self.found_check = tk.Checkbutton(self.input_frame, text="Found", variable=self.found_var, bg="#ffffff")
        self.found_check.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Image Upload Button
        self.upload_button = tk.Button(self.input_frame, text="Upload Image", command=self.upload_image, bg="#2196F3", fg="white", font=("Helvetica", 12))
        self.upload_button.grid(row=4, column=0, padx=10, pady=10)

        self.image_label = tk.Label(self.input_frame, bg="#ffffff")
        self.image_label.grid(row=4, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.input_frame, text="Add Item", command=self.add_item, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Search Frame
        self.search_frame = tk.Frame(master, bg="#e8f4f8")
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search:", bg="#e8f4f8")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(self.search_frame, width=30, font=("Helvetica", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_items)

        # Listbox Frame
        self.listbox_frame = tk.Frame(master, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(master, bg="#e8f4f8")
        self.buttons_frame.pack(pady=10)

        self.view_button = tk.Button(self.buttons_frame, text="View Details", command=self.view_item, bg="#2196F3", fg="white", font=("Helvetica", 12))
        self.view_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete Selected", command=self.delete_item, bg="#F44336", fg="white", font=("Helvetica", 12))
        self.delete_button.pack(side=tk.LEFT, padx=10)

        # Listbox to display items
        self.listbox = tk.Listbox(self.listbox_frame, font=("Helvetica", 12), bg="#ffffff", selectbackground="#d9e8f5")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Buttons Frame
       

    def upload_image(self):
        self.selected_image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if self.selected_image_path:
            self.show_image()

    def show_image(self):
        image = Image.open(self.selected_image_path)
        image.thumbnail((100, 100))
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)

    def add_item(self):
        item_text = self.item_entry.get()
        description_text = self.description_entry.get("1.0", tk.END).strip()
        contact_text = self.contact_entry.get()
        if item_text and description_text and contact_text:
            status = "Found" if self.found_var.get() else "Lost"
            self.items.append((item_text, description_text, contact_text, status, self.selected_image_path))
            self.update_listbox()
            self.clear_entries()
            self.image_label.config(image='')  # Clear displayed image
            self.selected_image_path = None
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def clear_entries(self):
        self.item_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        self.contact_entry.delete(0, tk.END)
        self.found_var.set(False)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)  # Clear current listbox
        for item, _, _, status, _ in self.items:
            self.listbox.insert(tk.END, f"{item} - {status}")

    def search_items(self, event):
        search_text = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)  # Clear current listbox
        for item in self.items:
            if search_text in item[0].lower() or search_text in item[1].lower():  # Search by item name or description
                self.listbox.insert(tk.END, f"{item[0]} - {item[3]}")  # Display matching items

    def view_item(self):
        try:
            selected_index = self.listbox.curselection()[0]
            item, description, contact, status, image_path = self.items[selected_index]
            
            # Create a new window for displaying item details
            details_window = tk.Toplevel(self.master)
            details_window.title("Item Details")
            details_window.geometry("400x400")

            # Display the details
            details = f"Item: {item}\nDescription: {description}\nContact: {contact}\nStatus: {status}"
            details_label = tk.Label(details_window, text=details, justify=tk.LEFT)
            details_label.pack(pady=10)

            # Show the image if it exists
            if image_path:
                image = Image.open(image_path)
                image.thumbnail((200, 200))  # Resize the image
                self.photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(details_window, image=self.photo)
                image_label.pack(pady=10)

            details_window.transient(self.master)  # Keep the new window above the main window
            details_window.grab_set()  # Make the new window modal
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an item to view details.")


    def delete_item(self):
        try:
            selected_index = self.listbox.curselection()[0]
            del self.items[selected_index]
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an item to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LostAndFoundApp(root)
    root.mainloop()
