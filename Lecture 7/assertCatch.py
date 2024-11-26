def square(x):
    return x * x

try:
    assert square(10) == 100
except AssertionError:
    print(f"Test Failed on square({10}), expected: {100}")


expected_values = [(2, 4), (4, 16), (7, 49), (0, 64), (9, 81)]

for (input, expected) in expected_values:
    if square(input) != expected:
        print(f"Test Failed on square({input}), expected: {expected}")

