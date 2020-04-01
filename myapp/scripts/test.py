from myapp.tasks import gen_prime
from time import sleep

primes = gen_prime.delay(100)
sleep(10)

if primes.ready():
    print(primes.get())
else:
    print('BAD WORk')












