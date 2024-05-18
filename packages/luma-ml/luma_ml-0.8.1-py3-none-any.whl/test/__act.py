import __local__
from luma.neural.layer import Activation

import matplotlib.pyplot as plt
import numpy as np


X = np.linspace(-5, 5, 100)

func = Activation.Swish()
out = func(X)
d_out = func.backward(X)

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

ax1.plot(X, out, c="dodgerblue", lw=2)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_title(f"{type(func).__name__} Function")
ax1.grid(alpha=0.4)

ax2.plot(X, d_out, c="orange", lw=2)
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_title(f"Backward Pass of {type(func).__name__} Function")
ax2.grid(alpha=0.4)

plt.tight_layout()
plt.show()
