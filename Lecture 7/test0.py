from prime import is_prime

def test_prime(n, expected):
    if is_prime(n) != expected:
        print(f"ERROR on is_prime({n}), expected {expected}")


# test_prime(5, True)
# test_prime(7, True)
# test_prime(99, False)

# test_prime(6, False)      # Remove Comment to find bug
# test_prime(8, False)      # Remove Comment to find bug 