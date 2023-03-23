import tkinter as tk
from tkinter import messagebox
from database import Database
from algorithm import ShortestPathFinder
import webbrowser


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Shortest Path Finder")
        self.database = Database("shopes.xlsx")
        self.addresses, self.names = self.database.get_address_and_names_by_category("בגדים")
        self.selected_names = []
        self.selected_addresses = []
        self.start_address = ""
        self.path_names = []
        self.path_points = []
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Select Shops:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.checkboxes = []
        for i, name in enumerate(self.names):
            var = tk.StringVar()
            cb = tk.Checkbutton(self.master, text=name, variable=var, font=("Arial", 12))
            cb.grid(row=i+1, column=0, sticky="w", padx=20)
            self.checkboxes.append((cb, var))
        tk.Label(self.master, text="Start Address:", font=("Arial", 14)).grid(row=len(self.names)+2, column=0, sticky="w", padx=10, pady=10)
        self.start_entry = tk.Entry(self.master, font=("Arial", 12), width=40)
        self.start_entry.grid(row=len(self.names)+3, column=0, sticky="w", padx=20)
        tk.Button(self.master, text="Find Shortest Path", font=("Arial", 12), command=self.calculate_shortest_path).grid(row=len(self.names)+4, column=0, pady=20)
        tk.Button(self.master, text="Show Map", font=("Arial", 12), command=self.show_map).grid(row=len(self.names)+5, column=0, pady=10)

    def calculate_shortest_path(self):
        self.selected_names.clear()
        self.selected_addresses.clear()
        for checkbox, var in self.checkboxes:
            if var.get() == "1":
                self.selected_names.append(checkbox.cget("text"))
                self.selected_addresses.append(self.addresses[self.names.index(checkbox.cget("text"))])
        if len(self.selected_addresses) < 2:
            messagebox.showerror("Error", "Please select at least two shops.")
            return
        self.start_address = self.start_entry.get()
        if not self.start_address:
            messagebox.showerror("Error", "Please enter a start address.")
            return
        self.path_names, self.path_points = ShortestPathFinder(self.start_address, self.selected_addresses, self.selected_names).get_shortest_path()
        messagebox.showinfo("Shortest Path", f"Shortest Path: {' -> '.join(self.path_names)}")

    def show_map(self):
        if not self.path_points:
            messagebox.showerror("Error", "Please calculate shortest path first.")
            return
        map_url = "https://www.google.com/maps/dir/"
        for point in self.path_points:
            map_url += f"{point[0]},{point[1]}/"
        webbrowser.open(map_url)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()