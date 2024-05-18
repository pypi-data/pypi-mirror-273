from luma.preprocessing.encoder import OneHotEncoder
from luma.neural.optimizer import AdamOptimizer
from luma.neural.network import *

import numpy as np

np.random.seed(42)

model = VGGNet_19(
    optimizer=AdamOptimizer(),
)
model.summarize(in_shape=(-1, 3, 224, 224))

# X = np.random.randn(100, 3, 224, 224)
# y = np.array(list(range(10)) * 10)
# y = OneHotEncoder().fit_transform(y.reshape(-1, 1))

# out = model.fit(X, y)
