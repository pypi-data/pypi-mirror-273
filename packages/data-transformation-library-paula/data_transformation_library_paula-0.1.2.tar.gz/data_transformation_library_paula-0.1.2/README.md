# Data Transformation Library by Paula

The `data-transformation-library-paula` is a Python package focused on providing essential tools for matrix operations and data transformations. These functions are fundamental for handling and processing data in areas like machine learning, signal processing, and image processing.

## Project Description

This package includes three key functionalities:

- `transpose2d`: Transposes a 2D matrix.
- `window1d`: Facilitates the generation of sliding windows over a 1D input array, ideal for time series analysis.
- `convolution2d`: Implements a 2D cross-correlation operation, which is pivotal in the field of image processing and neural networks.

These functions are crafted to support researchers, data scientists, and developers by simplifying complex operations into manageable, reusable components.

## Features

### Transpose
- Function: transpose2d(input_matrix)
- Input: input_matrix - a list of lists of real numbers.
- Output: Transposed matrix as a list of lists of real numbers.
- Required dependecies: Pure Python, using standard library.

### Time Series Windowing
- Function: window1d(input_array, size, shift=1, stride=1)
- Inputs:
  - input_array: List or 1D Numpy array of real numbers.
  - size: Integer, size (length) of the window.
  - shift: Integer, shift (step size) between windows.
  - stride: Integer, stride (step size) within each window.
- Output: List of lists or 1D Numpy arrays of real numbers.
- Required dependecies: Python and Numpy.

### Cross-Correlation
- Function: convolution2d(input_matrix, kernel, stride=1)
- Inputs:
  - input_matrix: 2D Numpy array of real numbers.
  - kernel: 2D Numpy array of real numbers.
  - stride: Integer, stride value.
- Output: 2D Numpy array of real numbers.
- Required dependecies: Python and Numpy.

## Installation

The library is available on PyPI and can be installed using pip:

```bash
pip install data-transformation-library-paula
```

## Usage
After installation, the functions can be imported and used in Python scripts or Jupyter notebooks.

Example usage:
```
from data_transformation_library_paula import transpose2d, window1d, convolution2d

# example for transpose2d
matrix = [[1, 2, 3], [4, 5, 6]]
transpose2d(matrix)

# example for window1d
input_array = [1, 2, 3, 4, 5, 6]
size = 3
shift = 2
window1d(input_array, size, shift)

# example for convolution2d
input_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
kernel = [[1, 0], [0, -1]]
stride = 2
convolution2d(input_matrix, kernel, stride)
```




