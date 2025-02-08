from closest import find_closest_pairs, ClosestPairsError

def main():
    """Test function for finding closest pairs."""
    points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
    m = 2
    try:
        result = find_closest_pairs(points, m)
        print("Closest pairs:", result)
    except ClosestPairsError as e:
        print(f"Error occurred: {e}")
if __name__ == "__main__":
    main()
