def mapper(matrix1, matrix2):
    mapped = []

    # Transpose matrix2 to easily access its columns
    matrix2_T = list(zip(*matrix2))

    for i, row in enumerate(matrix1):
        for j, col in enumerate(matrix2_T):
            # Map each cell computation (i, j)
            value = sum(a * b for a, b in zip(row, col))
            mapped.append((i, j, value))
    
    return mapped

def reducer(mapped_data, rows, cols):
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    for i, j, value in mapped_data:
        result[i][j] = value

    return result

# Main function
if __name__ == "__main__":
    # Example input matrices
    matrix1 = [
        [1, 2],
        [3, 4]
    ]

    matrix2 = [
        [5, 6],
        [7, 8]
    ]

    mapped = mapper(matrix1, matrix2)
    result = reducer(mapped, len(matrix1), len(matrix2[0]))

    # Print result matrix
    print("Result of Matrix Multiplication:")
    for row in result:
        print(row)
