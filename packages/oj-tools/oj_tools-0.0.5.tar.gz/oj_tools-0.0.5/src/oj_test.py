import oj


def prime_generator(hi):
    # Sieve of Eratosthenes
    # https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    sieve = [True] * (hi+1)
    for p in range(2, hi+1):
        if sieve[p]:
            for j in range(2*p, hi+1, p):
                sieve[j] = False
            yield p


PRIMES = list(prime_generator(200))

def get_nth_prime(n: int) -> int:
    assert n > 0
    return PRIMES[n-1]


if __name__ == '__main__':
    p = oj.Problem('prime')

    p.testcases['1'].input.write(f'{1}')
    p.testcases['1'].output.write(f'{get_nth_prime(1)}')

    p.testcases['2'].input.write(f'{2}')
    p.testcases['2'].output.write(f'{get_nth_prime(2)}')

    p.testcases['3'].input.write(f'{3}')
    p.testcases['3'].output.write(f'{get_nth_prime(3)}')

    p.testcases['4'].input.write(f'{4}')
    p.testcases['4'].output.write(f'{get_nth_prime(4)}')

    ...

    p.extract_as_dir()
