from luma.preprocessing.encoder import OneHotEncoder
from luma.neural.optimizer import AdamOptimizer
from luma.neural.network import ZFNet

import numpy as np

np.random.seed(42)

model = ZFNet(
    optimizer=AdamOptimizer(),
    out_features=10,
    batch_size=1,
    n_epochs=1,
    deep_verbose=True,
)
model.summarize(in_shape=(-1, 3, 227, 227))

X = np.random.randn(100, 3, 227, 227)
y = np.array(list(range(10)) * 10)
y = OneHotEncoder().fit_transform(y.reshape(-1, 1))

out = model.fit(X, y)
