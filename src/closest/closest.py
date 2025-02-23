from math import sqrt



class ClosestPairsError(Exception):
    """Custom exception for closest pairs errors."""
    pass

def euclidean_distance(point1, point2):
    """Computes the Euclidean distance between two points."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def merge_by_distance(left, right):
    """Merges two sorted lists based on distance."""
    merged_list = []
    i, j = 0, 0
    
    while i < len(left) and j < len(right):
        if left[i][2] <= right[j][2]:
            merged_list.append(left[i])
            i += 1
        else:
            merged_list.append(right[j])
            j += 1
    
    merged_list.extend(left[i:])
    merged_list.extend(right[j:])
    
    return merged_list

def merge_sort_closest_pairs(closest_pairs):
    """Sorts the list of closest pairs using merge sort."""
    if len(closest_pairs) <= 1:
        return closest_pairs
    
    mid = len(closest_pairs) // 2
    left_half = merge_sort_closest_pairs(closest_pairs[:mid])
    right_half = merge_sort_closest_pairs(closest_pairs[mid:])
    
    return merge_by_distance(left_half, right_half)

def find_closest_pairs(P):
    """Finds the m closest pairs from a list of points."""
    n = len(P)
   
    # Compute all pairwise distances
    closest_pairs = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            distance = euclidean_distance(P[i], P[j])
            closest_pairs.append((P[i], P[j], distance))
    
    # Sort the list using merge sort
    sorted_pairs = merge_sort_closest_pairs(closest_pairs)
    
    # Return the first m pairs with smallest distances
    return sorted_pairs
    #return closest_pairs

