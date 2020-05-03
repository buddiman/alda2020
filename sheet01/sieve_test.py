with open("sieve.py") as fp:
    exec(fp.read())

primes = sieve(1000)
print(primes)