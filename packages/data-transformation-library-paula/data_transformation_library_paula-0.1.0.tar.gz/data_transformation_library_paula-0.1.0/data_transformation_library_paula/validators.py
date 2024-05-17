from typing import Any
import numpy as np

def contains_only_real_numbers(array: np.ndarray) -> bool:
    """
    This function checks if the input array elements are real numbers only.
    Floating point numbers and integers are considered real.

    Parameters:
    array (np.ndarray): Input array that needs to be checked.

    Returns:
    bool: True if all elements are real numbers, False otherwise.
    """
    return array.dtype.kind in ['f', 'i']

def is_positive_integer(value: Any) -> bool:
    """
    This function checks if the input value is a positive integer.

    Parameters:
    value (Any): The input value that needs to be checked.

    Returns:
    bool: True if the input value is a positive integer, False otherwise.
    """
    return isinstance(value, int) and value > 0

def check_input_type(input_data: Any) -> str:
    """
    Check if the input is a list, a 1D array, or a 2D array.

    Args:
        input_data (Any): The input data to check. It can be of any type.

    Returns:
        str: A string indicating the type of the input. Possible return values are:
            - "1D list" if the input is a 1D list.
            - "2D list" if the input is a 2D list with consistent inner list lengths.
            - "1D np.ndarray" if the input is a 1D NumPy array.
            - "2D np.ndarray" if the input is a 2D NumPy array.
            - "Invalid input" if the input is inavlid for functions.
    """
    if isinstance(input_data, list):
        # check if input is a list of lists
        if all(isinstance(i, list) for i in input_data):
            # check if all nested lists have the same length
            inner_lengths = [len(inner_list) for inner_list in input_data]
            if len(set(inner_lengths)) == 1:
                # check if all elements in the 2D list are real numbers
                flat_list = [item for sublist in input_data for item in sublist]
                return "2D list" if contains_only_real_numbers(np.array(flat_list)) else "Invalid input"
            else:
                return "Invalid input"
        else:
            # check if all elements in the list are real numbers
            flat_list = list(input_data)
            return "1D list" if contains_only_real_numbers(np.array(flat_list)) else "Invalid input"
    
    elif isinstance(input_data, np.ndarray):
        # check the dimension of input array and whether the elements are real numbers
        if input_data.ndim == 1:
            return "1D np.ndarray" if contains_only_real_numbers(input_data) else "Invalid input"
        elif input_data.ndim == 2:
            return "2D np.ndarray" if contains_only_real_numbers(input_data) else "Invalid input"
        else:
            return "Invalid input"
    else:
        return "Invalid input"