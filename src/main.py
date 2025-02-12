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
     
        plt.style.use("dark_background")
        # Frame for input fields and button
        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(pady=10)

        # Input fields
        ttk.Label(self.input_frame, text="X:").grid(row=0, column=0, padx=5)
        self.x_entry = ttk.Entry(self.input_frame, width=8)
        self.x_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.input_frame, text="Y:").grid(row=0, column=2, padx=5)
        self.y_entry = ttk.Entry(self.input_frame, width=8)
        self.y_entry.grid(row=0, column=3, padx=5)

        # Add button
        self.add_button = ttk.Button(self.input_frame, text="Add Point", command=self.add_point)
        self.add_button.grid(row=0, column=4, padx=10)

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

