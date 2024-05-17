import numpy as np
from validators import check_input_type, is_positive_integer

def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    Transposes a given 2D matrix (list of lists of floats).
    
    Parameters:
        input_matrix (list[list[float]]): A 2D matrix to be transposed.
    
    Returns:
        list[list[float]]: The transposed matrix.

    Raises:
        ValueError: If input is not a list of lists of floats.
    """
    # validate input
    if check_input_type(input_matrix) != "2D list":
        raise ValueError("Invalid input: expected a 2D list of real numbers.")

    # create empty matrix
    transposed_matrix = [[] for _ in range(len(input_matrix[0]))]

    # transpose
    for row in input_matrix:
        for col_index, element in enumerate(row):
            transposed_matrix[col_index].append(element)

    return transposed_matrix

def window1d(input_array: list[float] | np.ndarray, 
             size: int, 
             shift: int = 1, 
             stride: int = 1) -> list[list[float]] | list[np.ndarray]:
    """
    Generates windows over a 1D input array with chosen size, shift, and stride.

    Parameters:
        input_array (list[float] | np.ndarray): A 1D array of real numbers.
        size (int): The number of elements in each window.
        shift (int): The step size between the start of each window.
        stride (int): The step size within each window for selecting elements.

    Returns:
        list[list[float]] | list[np.ndarray]: A list containing each window.

    Raises:
        ValueError: if input_array is not a 1D array/list of real numbers or parameters are invalid.
    """
    # validate input
    input_type = check_input_type(input_array)
    if input_type not in ["1D list", "1D np.ndarray"]:
        raise ValueError("Invalid input: expected a 1D list or 1D numpy array of real numbers.")

    # convert input list to np array
    if input_type == "1D list":
        input_array = np.array(input_array, dtype=float)

    # validate parameters
    if not is_positive_integer(stride):
        raise ValueError("Invalid input: stride must be a positive integer.")
    if not is_positive_integer(shift):
        raise ValueError("Invalid input: shift must be a positive integer.")
    if not is_positive_integer(size):
        raise ValueError("Invalid input: size must be a positive integer.")
    
    # get number of possible windows
    num_windows = ((len(input_array) - size) // shift) + 1
    if num_windows <= 0:
        return []

    windows = []
    for start in range(0, num_windows * shift, shift):
        end = start + size
        if end > len(input_array):
            break
        window = input_array[start:end:stride]

        if input_type == "1D list":
            windows.append(window.tolist())
        else:
            windows.append(window)

    return windows

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Performs a 2D cross-correlation operation on an input matrix with a given kernel.
    
    Parameters:
        input_matrix (np.ndarray): A 2D Numpy array of real numbers, representing the input image or feature map.
        kernel (np.ndarray): A 2D Numpy array of real numbers, representing the kernel or filter.
        stride (int): The number of elements to move the kernel by across the input_matrix. Must be a positive integer.

    Returns:
        np.ndarray: A 2D Numpy array containing the results of the cross-correlation operation.
    
    Raises:
        ValueError: if input_matrix or kernel is not 2D array or stride is not valid.
    """
    # validate input_matrix and kernel
    if check_input_type(input_matrix) != "2D np.ndarray":
        raise ValueError("Invalid input: input_matrix must be a 2D np.ndarray of real numbers.")
    if check_input_type(kernel) != "2D np.ndarray":
        raise ValueError("Invalid input: kernel must be a 2D np.ndarray of real numbers.")

    # validate the stride
    if not is_positive_integer(stride):
        raise ValueError("Invalid input: stride must be a positive integer")

    # dimensions of the input and kernel
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    # output dimensions
    output_height = ((input_height - kernel_height) // stride) + 1
    output_width = ((input_width - kernel_width) // stride) + 1

    # initialize output matrix
    output = np.zeros((output_height, output_width))

    # perform the cross-correlation
    for i in range(output_height):
        for j in range(output_width):
            row = i * stride
            col = j * stride
            output[i, j] = np.sum(input_matrix[row:row + kernel_height, col:col + kernel_width] * kernel)

    return output