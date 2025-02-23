import random
import time
import psutil
import tracemalloc
import threading
import datetime
from closest import find_closest_pairs

def generate_points(num_points):
    """Generates a list of random (x, y) points."""
    return [(random.uniform(-1000, 1000), random.uniform(-1000, 1000)) for _ in range(num_points)]

def monitor_cpu_usage(interval, stop_event, usage_list):
    # Initialize the measurement
    psutil.cpu_percent(interval=None)
    while not stop_event.is_set():
        usage = psutil.cpu_percent(interval=None)  # instantaneous reading
        usage_list.append(usage)
        time.sleep(interval)  # sample every `interval` seconds

def stress_test(num_points, writeToFile=False):
    output_file = "doc/results.txt"
    points = generate_points(num_points)
    
    # Set up CPU monitoring
    cpu_usage_list = []
    stop_event = threading.Event()
    monitor_thread = threading.Thread(
        target=monitor_cpu_usage, args=(0.1, stop_event, cpu_usage_list)
    )
    
    # Start memory profiling and CPU monitoring
    tracemalloc.start()
    monitor_thread.start()
    start_time = time.time()
    
    try:
        result = find_closest_pairs(points)
    except Exception as e:
        print(f"Error: {e}")
        stop_event.set()
        monitor_thread.join()
        return
    
    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Stop the CPU monitoring thread
    stop_event.set()
    monitor_thread.join()
    
    # Compute the average CPU usage during the computation
    avg_cpu_usage = sum(cpu_usage_list) / len(cpu_usage_list) if cpu_usage_list else 0

    #get the time stamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Prepare output results
    output_lines = [
        f"Timestamp: {timestamp}",
        f"Test with {num_points} points:",
        f"Execution time: {end_time - start_time:.4f} seconds",
        f"Memory used: {current_mem / 1024 / 1024:.2f} MB (Peak: {peak_mem / 1024 / 1024:.2f} MB)",
        f"Average CPU usage during computation: {avg_cpu_usage:.2f}%",
        "-" * 50
    ]
    
    # Print results
    print("\n".join(output_lines))
    
    # Optionally write to file
    if writeToFile:
        with open(output_file, "a") as f:
            f.write("\n".join(output_lines) + "\n")
