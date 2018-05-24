import json
import unittest
import itertools

def greatest_common_divisor(p, q):
	return p if q is 0 else greatest_common_divisor(q, p%q)

def least_common_multiple(p, q):
	return int((p*q) / greatest_common_divisor(p, q))

def coprimes_of(t):
	return [e for e in range(2, t) if greatest_common_divisor(e, t) == 1]

def modular_multiplicative_inverse(a, modulus):
	for x in itertools.count():
		if (a*x) % modulus == 1:
			return x

class RSA:
	def __init__(self, p, q, coprime_index):
		self.p = p
		self.q = q
		self.n = p*q
		self.t = least_common_multiple(self.p-1, self.q-1)
		self.e = coprimes_of(self.t)[coprime_index]
		self.d = modular_multiplicative_inverse(self.e, self.t)

	def encrypt(self, x):
		return (x ** self.e) % self.n

	def decrypt(self, x):
		return (x ** self.d) % self.n

	def test(self, original_message):
		cipher = self.encrypt(original_message)
		recovered_message = self.decrypt(cipher)
		success = original_message == recovered_message
		return [cipher, success]

	def __repr__(self):
		return json.dumps(self.__dict__)

def test_rsa(p, q, coprime_index, m):
	rsa = RSA(p, q, coprime_index)
	result = rsa.test(m)
	print(rsa)
	return result

class Tests(unittest.TestCase):
	def test_func(self):
		for func, input, expected_output in [
			(greatest_common_divisor, (48, 0), 48),
			(greatest_common_divisor, (48, 18), 6),
			(greatest_common_divisor, (18, 48), 6),
			(greatest_common_divisor, (60, 52), 4),
			(least_common_multiple, (60, 52), 780),
			(coprimes_of, (9,), [2, 4, 5, 7, 8]),
			(modular_multiplicative_inverse, (17, 780), 413),
			(test_rsa, (61, 53, 2, 100), [1773, True]),
			(test_rsa, (61, 53, 0, 100), [2872, True]),
			(test_rsa, (17, 53, 4, 100), [876, True]),
			(test_rsa, (197, 53, 3, 100), [9992, True]),
			(test_rsa, (199, 53, 0, 100), [9608, True]),
		]:
			actual_output = func(*input)
			print(func.__name__, input, actual_output, expected_output)
			self.assertEqual(actual_output, expected_output)
if __name__ == '__main__':
	unittest.main()
