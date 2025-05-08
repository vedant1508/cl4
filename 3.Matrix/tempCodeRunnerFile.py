from collections import defaultdict
from multiprocessing import Pool

# Sample matrices A (m x n) and B (n x p)
A = [
    [1, 2],
    [3, 4]
]  # 2x2

B = [
    [5, 6],
    [7, 8]
]  # 2x2

# Convert A and B to key-value pairs for mapper
def create_key_value_pairs(A, B):
    key_values = []

    # Matrix A emits: ((i, k), ("A", i, k, A[i][k]))
    for i in range(len(A)):
        for k in range(len(A[0])):
            key_values.append(("A", i, k, A[i][k]))

    # Matrix B emits: ((k, j), ("B", k, j, B[k][j]))
    for k in range(len(B)):
        for j in range(len(B[0])):
            key_values.append(("B", k, j, B[k][j]))

    return key_values

# Mapper function
def mapper(record):
    tag, i_or_k, k_or_j, value = record
    mapped = []

    if tag == "A":
        for j in range(len(B[0])):
            # Key: (i, j) - Result matrix position
            # Emit A[i][k] with matching B[k][j]
            mapped.append(((i_or_k, j), ("A", k_or_j, value)))
    elif tag == "B":
        for i in range(len(A)):
            mapped.append(((i, k_or_j), ("B", i_or_k, value)))
    return mapped

# Reducer function
def reducer(intermediate):
    results = defaultdict(list)

    # Group by key
    for key, values in intermediate.items():
        a_vals = {}
        b_vals = {}

        for tag, k, val in values:
            if tag == "A":
                a_vals[k] = val
            else:
                b_vals[k] = val

        total = 0
        for k in a_vals:
            if k in b_vals:
                total += a_vals[k] * b_vals[k]

        return (key, total)

# Main function
def matrix_multiply(A, B):
    key_value_pairs = create_key_value_pairs(A, B)

    # Simulate mapper phase
    with Pool() as pool:
        mapped = pool.map(mapper, key_value_pairs)

    # Flatten mapped output
    flattened = [item for sublist in mapped for item in sublist]

    # Group by key
    intermediate = defaultdict(list)
    for key, value in flattened:
        intermediate[key].append(value)

    # Reduce phase
    result = defaultdict(int)
    for key in sorted(intermediate):
        key_out, val_out = reducer({key: intermediate[key]})
        result[key_out] = val_out

    # Convert result to matrix form
    rows = len(A)
    cols = len(B[0])
    final_matrix = [[0] * cols for _ in range(rows)]
    for (i, j), val in result.items():
        final_matrix[i][j] = val

    return final_matrix

# Run and display result
result_matrix = matrix_multiply(A, B)
print("Result Matrix:")
for row in result_matrix:
    print(row)
    