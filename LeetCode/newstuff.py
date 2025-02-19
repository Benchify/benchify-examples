def matrix_multiply(A, B):
    """
    Multiply two matrices A and B.
    Returns None if matrices cannot be multiplied.
    """
    if not A or not B or len(A[0]) != len(B):
        return None
        
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
                
    return result

def fast_power(base, exponent, modulus=None):
    """
    Calculate base^exponent efficiently using binary exponentiation.
    Optional modulus parameter for modular exponentiation.
    """
    if exponent < 0:
        raise ValueError("Negative exponents not supported")
    
    result = 1
    while exponent > 0:
        if exponent & 1:  # If exponent is odd
            result = result * base
            if modulus:
                result %= modulus
        base = base * base
        if modulus:
            base %= modulus
        exponent >>= 1  # Divide exponent by 2
        
    return result

def sieve_of_eratosthenes(n):
    """
    Find all prime numbers up to n using the Sieve of Eratosthenes algorithm.
    Returns a list of prime numbers.
    """
    if n < 2:
        return []
        
    # Initialize boolean array "is_prime[0..n]"
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    # Use Sieve of Eratosthenes to mark non-prime numbers
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            # Mark all multiples of i as non-prime
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    # Collect all prime numbers
    return [i for i in range(n + 1) if is_prime[i]]

