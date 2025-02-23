from closest import find_closest_pairs, ClosestPairsError
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stress_test import stress_test

# Run stress tests
#stress_test(1000, 10)   # Small dataset
#stress_test(5000, 50)   # Medium dataset
#stress_test(10000, 100) # Large dataset
#stress_test(50000, 500) # Very large dataset

# Solarized Dark Colors
SOLARIZED_BG = "#002b36"
SOLARIZED_AXES_BG = "#073642"
SOLARIZED_TEXT = "#839496"
SOLARIZED_GRID = "#586e75"
SOLARIZED_POINT_PRIMARY = "#b58900"
SOLARIZED_POINT_SECONDARY = "#cb4b16"
SOLARIZED_ENTRY_BG = "#073642"
SOLARIZED_ENTRY_TEXT = "#839496"
SOLARIZED_CURSOR = "#b58900"

# Sample points
points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]

class PointsPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Closest Pairs Visualizer")
        self.root.configure(bg=SOLARIZED_BG)
        self.root.minsize(650, 600)
        

        # Counter variable
        self.find_counter_var = tk.StringVar(value="1")  # Default value set to 1

        # Left Panel for Points List
        self.main_frame = ttk.Frame(root, style="Solarized.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.left_frame = ttk.Frame(self.main_frame, style="Solarized.TFrame")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, anchor="center")
        
        points_label_frame = ttk.Frame(self.left_frame, style="Solarized.TFrame")
        points_label_frame.pack(fill=tk.X)
        ttk.Label(points_label_frame, text="Points List", style="Solarized.TLabel").pack(side=tk.LEFT)
        
        #button to spawn the add point sub menu
        add_point_button = ttk.Button(points_label_frame, text="+", style="Solarized.TButton", command=self.open_add_point_popup)
        add_point_button.pack(side=tk.RIGHT, padx=(10, 0))

        # button to run the stress test
        stress_button = ttk.Button(points_label_frame, text="stress", style="Solarized.TButton", command=self.run_stress_test)
        stress_button.pack(side=tk.RIGHT)
       
        # Frame for Find button and counter
        find_frame = ttk.Frame(points_label_frame, style="Solarized.TFrame")
        find_frame.pack(side=tk.RIGHT, padx=8)
        
        find_closest_button = ttk.Button(find_frame, text="Find", style="Solarized.TButton", command=self.find_and_plot_closest_pairs)
        find_closest_button.pack(side=tk.LEFT)

        # Counter label
        self.find_counter_entry = ttk.Entry(find_frame, textvariable=self.find_counter_var, width=5, justify="center", style="Solarized.TEntry")
        self.find_counter_entry.pack(side=tk.LEFT, padx=5)

        self.points_listbox = tk.Listbox(self.left_frame, bg=SOLARIZED_ENTRY_BG, fg=SOLARIZED_ENTRY_TEXT)
        self.points_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Frame for Matplotlib graph
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.fig.patch.set_facecolor(SOLARIZED_BG)
        self.ax.set_facecolor(SOLARIZED_AXES_BG)

        self.setup_styles()
        self.plot_points(points)
        self.update_points_list()

    def setup_styles(self):
        plt.style.use("dark_background")
        style = ttk.Style()
        style.configure("Solarized.TEntry", fieldbackground=SOLARIZED_ENTRY_BG, foreground=SOLARIZED_ENTRY_TEXT, insertcolor=SOLARIZED_CURSOR)
        style.configure("Solarized.TFrame", background=SOLARIZED_BG)
        style.configure("Solarized.TButton", padding=(5, 2), background=SOLARIZED_AXES_BG, foreground=SOLARIZED_TEXT, borderwidth=1, relief="flat")
        style.map("Solarized.TButton", background=[("active", SOLARIZED_GRID), ("pressed", SOLARIZED_POINT_SECONDARY)])
        style.configure("Solarized.TLabel", background=SOLARIZED_BG, foreground=SOLARIZED_TEXT)
        style.configure("Solarized.TCombobox", 
                    fieldbackground=SOLARIZED_ENTRY_BG,   # Background for the text field
                    background=SOLARIZED_BG,                # Overall background of the widget
                    foreground=SOLARIZED_TEXT,              # Text color
                    arrowcolor=SOLARIZED_CURSOR)            # Color of the drop-down arrow
        


    def open_add_point_popup(self):
        """Opens a popup window for adding a new point."""
        popup = tk.Toplevel(self.root)
        popup.title("Add Point")
        popup.configure(bg=SOLARIZED_BG)
        
        ttk.Label(popup, text="X:", style="Solarized.TLabel").grid(row=0, column=0, padx=5, pady=5)
        x_entry = ttk.Entry(popup, width=8, style="Solarized.TEntry")
        x_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(popup, text="Y:", style="Solarized.TLabel").grid(row=1, column=0, padx=5, pady=5)
        y_entry = ttk.Entry(popup, width=8, style="Solarized.TEntry")
        y_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def add_point_from_popup():
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                points.append((x, y))
                self.plot_points(points)
                self.update_points_list()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for X and Y.")
        
        button_frame = ttk.Frame(popup, style="Solarized.TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Point", style="Solarized.TButton", command=add_point_from_popup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", style="Solarized.TButton", command=popup.destroy).pack(side=tk.RIGHT, padx=5)
        
    def run_stress_test(self):
        popup = tk.Toplevel(self.root)
        popup.title("Run Stress test")
        popup.configure(bg=SOLARIZED_BG)

        ttk.Label(popup, text="Level of stress: ", style="Solarized.TLabel").grid(row=0, column=0, padx=5, pady=5)
        
        # Define your four options
        stress_options = ["Low", "Medium", "High", "Extreme"]

        # Create a Combobox with the options and set it to be readonly
        stress_combobox = ttk.Combobox(popup, values=stress_options, state="readonly", style="Solarized.TCombobox")
        stress_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        #check box to write to file
        write_to_file_var = tk.BooleanVar(value=False)
        write_to_file_checkbox = tk.Checkbutton(popup,
                                            text="Write to file",
                                            variable=write_to_file_var,
                                            bg=SOLARIZED_BG,
                                            fg=SOLARIZED_TEXT,
                                            activebackground=SOLARIZED_BG,
                                            activeforeground=SOLARIZED_TEXT,
                                            selectcolor=SOLARIZED_ENTRY_BG,
                                            highlightthickness=0,
                                            borderwidth=0,
                                            relief="flat")


        write_to_file_checkbox.grid(row=0, column=2, padx=5, pady=5)
        # Optionally, set a default selection (index 0 here)
        stress_combobox.current(0)

        button_frame = ttk.Frame(popup, style="Solarized.TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="Run Stress",
            style="Solarized.TButton",
            command=lambda: self.stress_wrapper(stress_combobox.get(), write_to_file_var.get())
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame,
            text="Cancel",
            style="Solarized.TButton",
            command=popup.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def stress_wrapper(self, stress_option, write_to_file):
        if stress_option == "Low":
            stress_test(100, write_to_file)
        elif stress_option == "Medium":
            stress_test(200, write_to_file)
        elif stress_option == "High":
            stress_test(400, write_to_file)
        elif stress_option == "Extreme":
            stress_test(800, write_to_file)
        else:
            print("you should never see this")

    def plot_points(self, points):
        self.ax.clear()
        self.ax.set_title("Points Visualization", color=SOLARIZED_TEXT)
        self.ax.set_xlabel("X-axis", color=SOLARIZED_TEXT)
        self.ax.set_ylabel("Y-axis", color=SOLARIZED_TEXT)
        self.ax.tick_params(colors=SOLARIZED_TEXT)
        self.ax.grid(True, color=SOLARIZED_GRID, linestyle="--", linewidth=0.5)
        
        if points:
            x_vals, y_vals = zip(*points)
            colors = [SOLARIZED_POINT_PRIMARY]
            self.ax.scatter(x_vals, y_vals, c=colors, edgecolors="white", zorder = 2)
            
            for (x, y) in points:
                self.ax.text(x, y, f"({x}, {y})", fontsize=10, verticalalignment="bottom", color=SOLARIZED_TEXT)
        
        self.canvas.draw()
    
    def add_point(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            points.append((x, y))
            self.plot_points(points)
            self.update_points_list()
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for X and Y.")
    
    def update_points_list(self):
        self.points_listbox.delete(0, tk.END)
        for p in points:
            self.points_listbox.insert(tk.END, str(p))
    
    def find_and_plot_closest_pairs(self):
        """Find and plot closest pairs using the user-defined counter."""
        if len(points) < 2:
            messagebox.showwarning("Not Enough Points", "Please add at least two points.")
            return

        try:
            # Retrieve the user-defined number from the entry field
            num_lines = int(self.find_counter_var.get())  # Convert entry to integer
            
            # Ensure the value is valid
            if num_lines < 1:
                messagebox.showerror("Invalid Input", "Please enter a positive integer.")
                return
            
            closest_pair = find_closest_pairs(points)
            print(closest_pair)
            
            # Use the user-defined value for the number of lines to draw
            self.draw_lines_from_closest_pairs(closest_pair, num_lines)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
        except ClosestPairsError as e:
            print("Error", f"Could not find closest pair: {e}")

    def draw_lines_from_closest_pairs(self, closest_pairs, x):
        """Draws lines between the first x closest pairs of points."""
        self.plot_points(points)  # Redraw the base plot first

        if x > len(closest_pairs):
            x = len(closest_pairs)  # Limit x to the available pairs

        for i in range(x):
            p1, p2, distance = closest_pairs[i]
            x_vals = [p1[0], p2[0]]
            y_vals = [p1[1], p2[1]]

            # Plot a line between the two points
            self.ax.plot(
                x_vals, y_vals, 
                color="cyan", linestyle="-", linewidth=2, 
                label=f"Dist: {distance:.2f}"
            )

        self.canvas.draw()  # Update the canvas\

    def draw_lines_from_closest_pairs(self, closest_pairs, x):
        """Draws lines between the first x closest pairs of points with different colors."""
        self.plot_points(points)  # Redraw the base plot first

        if x > len(closest_pairs):
            x = len(closest_pairs)  # Limit x to the available pairs

        # Generate distinct colors for each pair
        colors = [(
            random.random(),  # Red component
            random.random(),  # Green component
            random.random()   # Blue component
        ) for _ in range(x)]

        for i in range(x):
            p1, p2, distance = closest_pairs[i]
            x_vals = [p1[0], p2[0]]
            y_vals = [p1[1], p2[1]]

            # Plot a line between the two points with a unique color
            self.ax.plot(
                x_vals, y_vals, 
                color=colors[i], linestyle="-", linewidth=2, 
                label=f"Pair {i+1} (Dist: {distance:.2f})",
                zorder=1  # Ensure lines are drawn behind the points
            )
            # Redraw the points to make sure they are on top
        self.ax.scatter(
            [p[0] for p in points], 
            [p[1] for p in points], 
            color=[SOLARIZED_POINT_PRIMARY],
            edgecolors='white',
            s=50, 
            zorder=2  # Ensure dots appear on top
        )       
        self.ax.legend()  # Show the legend with the colored lines
        self.canvas.draw()  # Update the canvas

if __name__ == "__main__":
    root = tk.Tk()
    app = PointsPlotterApp(root)
    root.mainloop()
