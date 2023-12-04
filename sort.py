import pandas as pd
import sys

# increase recursion limit for quick sort
sys.setrecursionlimit(5000)

def handle_category(category):
    # convert the given category to the correct column name in the dataframe
    if category == 'price':
        return 'Price'
    elif category == 'install':
        return 'Approximate Installs'
    else:  # else return Rating as default
        return 'Rating'

def mergesort(df, category):
    # set up variables needed for merge sort
    sort_by = handle_category(category)
    mergesort_helper(df, sort_by)
    return df

# referenced the lecture slides on sorting
def mergesort_helper(df, category):
    if len(df) > 1:
        # find midpoint index and divide original array
        middle = len(df) // 2
        left_side = df.iloc[:middle].copy()
        right_side = df.iloc[middle:].copy()

        # merge sort on subarrays
        mergesort_helper(left_side, category)
        mergesort_helper(right_side, category)

        # merge sorted subarrays
        merge(df, category, left_side, right_side)

def merge(df, category, left, right):
    i, j, k = 0, 0, 0

    # compare and sort the two arrays
    while i < len(left) and j < len(right):
        if left[category].iloc[i] > right[category].iloc[j]:
            df.iloc[k] = left.iloc[i]
            i += 1
        else:
            df.iloc[k] = right.iloc[j]
            j += 1
        k += 1

    # append remaining elements in left or right
    while i < len(left):
        df.iloc[k] = left.iloc[i]
        i += 1
        k += 1

    while j < len(right):
        df.iloc[k] = right.iloc[j]
        j += 1
        k += 1

def quicksort(df, category):
    # set up variables for quick sort
    sort_by = handle_category(category)
    quicksort_helper(df, sort_by, 0, len(df) - 1)
    return df

# referenced lecture slides on sorting
def quicksort_helper(df, category, low, high):
    if low < high:
        piv = partition(df, category, low, high)
        quicksort_helper(df, category, low, piv - 1)
        quicksort_helper(df, category, piv + 1, high)

def partition(df, category, low, high):
    # define pivot and initialize up and down
    piv = df[category].iloc[low]
    up, down = low, high
    
    while up < down:
        # increase up until value at up is less than pivot or up reaches high
        while up <= high and df[category].iloc[up] >= piv:
            up += 1
        # decrease down until value at down is greater than pivot or down reaches low
        while df[category].iloc[down] < piv:
            down -= 1
        if up < down:
            # swap up and down
            df.iloc[up], df.iloc[down] = df.iloc[down].copy(), df.iloc[up].copy()
    
    # swap low and down
    df.iloc[low], df.iloc[down] = df.iloc[down].copy(), df.iloc[low].copy()
    return down