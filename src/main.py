from closest import find_closest_pairs, ClosestPairsError
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Solarized Dark Colors
SOLARIZED_BG = "#002b36"
SOLARIZED_AXES_BG = "#073642"
SOLARIZED_TEXT = "#839496"
SOLARIZED_GRID = "#586e75"
SOLARIZED_POINT_PRIMARY = "#b58900"
SOLARIZED_POINT_SECONDARY = "#cb4b16"
SOLARIZED_ENTRY_BG = "#073642"  # Dark cyan from Solarized
SOLARIZED_ENTRY_TEXT = "#839496"  # Light gray-blue text
SOLARIZED_CURSOR = "#b58900"  # Yellow cursor
# Sample points
points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]


class PointsPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Closest Pairs Visualizer")
        self.root.configure(bg=SOLARIZED_BG)  # Set background color
        # Frame for Matplotlib graph
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.fig.patch.set_facecolor(SOLARIZED_BG)  # Figure background
        self.ax.set_facecolor(SOLARIZED_AXES_BG)  # Axes background

        #Styles     
        plt.style.use("dark_background")
        style = ttk.Style()
        style.configure("Solarized.TEntry",
                fieldbackground=SOLARIZED_ENTRY_BG,  # Background color
                foreground=SOLARIZED_ENTRY_TEXT,    # Text color
                insertcolor=SOLARIZED_CURSOR)       # Cursor color

        # Set frame background color
        style.configure("Solarized.TFrame",
                background=SOLARIZED_BG,  # Frame background color
                )
        # Set button styling
        style.configure("Solarized.TButton",
                padding=(5, 2),
                background=SOLARIZED_AXES_BG,   # Background of the button
                foreground=SOLARIZED_TEXT,      # Text color
                borderwidth=1,
                relief="flat")  # Remove 3D effect

        style.map("Solarized.TButton",
                   background=[("active", SOLARIZED_GRID), ("pressed", SOLARIZED_POINT_SECONDARY)])

        # Set label styling
        style.configure("Solarized.TLabel",
                background=SOLARIZED_BG,  # Background color
                foreground=SOLARIZED_TEXT)  # Text color

        # Frame for input fields and button
        # Outer tk.Frame (border color)
        self.frame_wrapper = tk.Frame(root, bg=SOLARIZED_GRID)
        self.frame_wrapper.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Inner ttk.Frame (styled with Solarized theme)
        self.input_frame = ttk.Frame(self.frame_wrapper, style="Solarized.TFrame")
        self.input_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Ensure the frame itself expands fully
        self.input_frame.columnconfigure(0, weight=1)  # Left padding
        self.input_frame.columnconfigure(1, weight=1)  # X Label
        self.input_frame.columnconfigure(2, weight=1)  # X Entry
        self.input_frame.columnconfigure(3, weight=1)  # Y Label
        self.input_frame.columnconfigure(4, weight=1)  # Y Entry
        self.input_frame.columnconfigure(5, weight=1)  # Button
        self.input_frame.columnconfigure(6, weight=1)  # Right padding

        self.input_frame.rowconfigure(0, weight=1)  # Ensure vertical centering

        # X Label
        ttk.Label(self.input_frame, text="X:", style="Solarized.TLabel").grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # X Entry
        self.x_entry = ttk.Entry(self.input_frame, width=8, style="Solarized.TEntry")
        self.x_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Y Label
        ttk.Label(self.input_frame, text="Y:", style="Solarized.TLabel").grid(row=0, column=3, padx=5, pady=5, sticky="e")

        # Y Entry
        self.y_entry = ttk.Entry(self.input_frame, width=8, style="Solarized.TEntry")
        self.y_entry.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Add Button
        self.add_button = ttk.Button(self.input_frame, text="Add Point", style="Solarized.TButton", command=self.add_point)
        self.add_button.grid(row=0, column=5, padx=10, pady=5, sticky="ew")

        # Center contents inside the frame
        self.input_frame.grid_propagate(False)  # Prevent auto-resizing
        # Plot initial points
        self.plot_points(points)

    def plot_points(self, points):
        """Plots the given list of points on the graph."""
        self.ax.clear()  # Clear previous plot
        self.ax.set_title("Points Visualization", color=SOLARIZED_TEXT)
        self.ax.set_xlabel("X-axis", color=SOLARIZED_TEXT)
        self.ax.set_ylabel("Y-axis", color=SOLARIZED_TEXT)
        self.ax.tick_params(colors=SOLARIZED_TEXT)
        self.ax.grid(True, color=SOLARIZED_GRID, linestyle="--", linewidth=0.5)

        if points:
            x_vals, y_vals = zip(*points)
            colors = [SOLARIZED_POINT_PRIMARY if i % 2 == 0 else SOLARIZED_POINT_SECONDARY for i in range(len(points))]
            self.ax.scatter(x_vals, y_vals, c=colors, edgecolors="white", label="Points")

            # Annotate each point
            for (x, y) in points:
                self.ax.text(x, y, f"({x}, {y})", fontsize=10, verticalalignment="bottom", color=SOLARIZED_TEXT)

        self.ax.legend(facecolor=SOLARIZED_AXES_BG, edgecolor="white")
        self.canvas.draw()  # Redraw canvas

    def add_point(self):
        """Adds a new point to the list and updates the plot."""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            points.append((x, y))  # Update global points list
            self.plot_points(points)  # Refresh graph
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for X and Y.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PointsPlotterApp(root)
    root.mainloop()

