from itertools import product


domain_two = {(i, j) for i, j in product(range(2), repeat=2)}
print(domain_two)
print('aaaaaaaaaaaaaaaa')
domain_two = product(range(10), repeat=2)
print(domain_two)