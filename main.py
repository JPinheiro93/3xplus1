import time
from typing import Callable
import numpy as np
import functools


def next(n: int) -> int:
	return int(n // 2) if n % 2 == 0 else int(3 * n + 1)


def next_k(n: int, k: int) -> int:
	return functools.reduce(lambda x, _: next(x), range(k), n)


def power_k(k: int) -> int:
	return 2 ** (k + 1)


def can_ignore_now(n: int) -> bool:
	return n % 4 in [0, 1, 2]


def can_ignore_k(n: int, k: int) -> bool:
	resulting_number = next_k(n, k)
	return resulting_number in [4, 2, 1] or resulting_number % power_k(k) == 0


def can_ignore_until_k(n: int, k: int, prev: bool) -> bool:
	if prev == True:
		return True
	return can_ignore_until_k(n, k+1, can_ignore_k(n, k))

# A: any number such that next(n) is in the form 4n can be ignored
# A+ (generelization of A): any number such that next_k(n, k) is in the form 2^(k+1) * c can be ignored
# any number in the form 4n can be ignored
# any number in the form 4n+1 can be ignored
# any number in the form 4n+2 can be ignored


def can_ignore(n: int) -> bool:
	return can_ignore_until_k(n, 1, can_ignore_now(n))


def hailstone_chain(seed: int) -> set:
	x: int = seed
	current_chain: set[int] = []
	while not x in current_chain:
		current_chain.append(x)
		x = next(x)
	return current_chain


def collatz(seed: int) -> list:
	x: int = next(seed)
	current_chain: set[int] = [seed]
	while x > seed:
		current_chain.append(x)
		x = next(x)
	current_chain.append(x)
	return current_chain


def test_until_power_k(x: int) -> None:
	seeds: set[int] = np.arange(3, x, 4)
	results = [(n, can_ignore(n)) for n in seeds]
	undefined: list[int] = [r[0] for r in results if r[1] == False]
	if len(undefined) > 0:
		print("COUNTER EXAMPLES FOUND: %d" % undefined)
	return


def test_until_hailstone(x: int) -> None:
	seeds: set[int] = np.flip(np.arange(3, x, 4))
	m = len(seeds)
	while m > 0:
		i = seeds[0]
		chain = hailstone_chain(i)
		if chain[-1] == 1:
			seeds = np.flip(np.setdiff1d(seeds, chain))
			m = len(seeds)
		else:
			print("COUNTER EXAMPLE FOUND: %d" % i)
			break
	return

def test_until_collatz(x: int) -> None:
	seeds: set[int] = np.flip(np.arange(3, x, 4))
	m = len(seeds)
	while m > 0:
		i = seeds[0]
		chain = collatz(i)
		seeds = np.flip(np.setdiff1d(seeds, chain))
		m = len(seeds)
	return


def test(x: int, f: Callable[[int], None]) -> None:
	start_time = time.time()
	f(x)
	end_time = time.time()
	print("Test: %s in %s seconds." % (f.__name__, end_time - start_time))
	return


if __name__ == "__main__":
	x: int = 1 * 10 ** 4 + 27

	#1- Test applying next(n), k times, until hitting a number in the form 2^(k+1) * c, c being any positive integer
	#test(x, test_until_power_k)
	#2- Test all chains, remove all found numbers until now from testing set
	test(x, test_until_hailstone)
	#3- Test all chains (until a number lower than the original seed is found), remove all found numbers until now from testing set
	test(x, test_until_collatz)
