# Closest Pairs Visualizer

This project provides a graphical interface for visualizing a set of 2D points and identifying the closest pairs among them. It also includes a stress test utility to gauge performance, CPU usage, and memory usage under different workloads.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Graphical Application](#running-the-graphical-application)
  - [GUI Overview](#gui-overview)
  - [Stress Test Utility](#stress-test-utility)
- [Dependencies](#dependencies)
- [License](#license)

---


- **closest.py**  
  - Contains functions and logic to compute the closest pairs of points.  
  - Uses a merge sort–based approach to sort pairs by distance.
  - Main functions include:
    - `euclidean_distance(point1, point2)`: Calculates the Euclidean distance between two points.
    - `merge_sort_closest_pairs(closest_pairs)`: Sorts the pairs list by distance using merge sort.
    - `find_closest_pairs(P)`: Returns all pairwise distances among points, sorted from smallest to largest.

- **stress_test.py**  
  - Generates random points and measures the performance and resource usage (CPU, memory) of the `find_closest_pairs` function.
  - Periodically samples CPU usage and uses Python’s `tracemalloc` to track memory usage.
  - Main functions include:
    - `generate_points(num_points)`: Creates a list of random (x, y) coordinates.
    - `stress_test(num_points, writeToFile=False)`: Runs the closest pairs operation on a large set of generated points, recording execution time, average CPU usage, and memory usage.

- **main.py**  
  - Provides a GUI built with Tkinter to load, display, and manage 2D points.
  - Integrates Matplotlib to plot points and draw lines between the closest pairs.
  - Also includes a sub-menu to run various stress tests at different levels of intensity.
  - To run the GUI, simply execute `python main.py`.

---

## Features

1. **GUI for Plotting Points**  
   - Displays points on a 2D plane using Matplotlib.  
   - Automatically updates when new points are added.

2. **Closest Pairs Computation**  
   - Dynamically compute and visualize the _m_ closest pairs as lines drawn between points.
   - Customize the number of lines to display via a simple input field.

3. **Stress Testing**  
   - Generate large sets of random points (ranging from 100 to 800+ points) and measure:
     - Execution time for finding closest pairs.
     - Memory usage and peak memory usage.
     - CPU utilization over the runtime.

4. **Customization**  
   - Uses a Solarized Dark color scheme for the GUI.  
   - Easily adjust the number of points or color styles in the code.

---

## Installation

1. **Clone the Repository**     
```bash
   git clone https://github.com/your-username/closest-pairs-visualizer.git
   cd closest-pairs-visualizer
```
2. **Install Requirements**
```bash
    pip install -r requirements.txt
```
for whatever reason if thats not working 
```bash
    pip install tkinter matplotlib psutil
```

3. ** Run the application **
```bash
    python3 src/main.py
```

**GUI Overview**

    Points List
        On the left, you’ll see a listbox showing all currently loaded points.

    Add Point
        Click the + button to open a small popup.
        Enter the X and Y coordinates (floats allowed) and click Add Point.
        The new point is added to the internal list and plotted in real-time.

    Stress Test
        Click the stress button to open a popup that allows you to pick:
            Stress level: Low, Medium, High, or Extreme.
            Optionally “Write to file” to record test results in doc/results.txt.
        Clicking Run Stress will execute a performance test and print the results in the console (and possibly write to a file).

    Finding Closest Pairs
        Use the “Find” button to compute closest pairs among all listed points.
        Specify how many pairs to highlight by changing the number in the adjacent text box (default is 1).
        The lines connecting each of the “closest pairs” are drawn on the plot in different colors.

    Matplotlib Plot
        The main panel shows all the loaded points.
        When you click “Find,” lines are drawn between the specified number of closest pairs.


**Dependencies**

    Python 3.7+
    Tkinter: For the GUI (usually comes with most Python distributions).
    Matplotlib: For plotting points and lines.
    psutil: For measuring CPU usage.
    tracemalloc: For monitoring memory allocations (included in Python’s standard library
