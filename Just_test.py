import numpy as np
import matplotlib.pyplot as plt
from math import factorial

def bin_dist(k, n, p):
    nck = factorial(n) / (factorial(k) * factorial(n - k))
    pd = nck * p**k * (1-p)**(n-k)
    return pd

# n = 당첨 횟수
# p = 확률
# k = 시행 횟수
n = 4
p = 0.03 * 0.5
k = 5

# x = np.arange(16)
# pd1 = np.array([bin_dist(k, n, p) for k in range(16)])
# plt.ylim(0, 0.3)
# plt.text(12.5, 0.28, 'n, p = 15, 0.3')
# plt.bar(x, pd1, color='lightcoral')
# plt.show()

print(bin_dist(n, k, p))