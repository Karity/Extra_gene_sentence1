import torch
import numpy as np

a = torch.rand((3, 4))
b = torch.rand((3, 4))
print(a, '\n', b)

print(torch.cat([a, b], dim=0))

print(torch.stack([a, b]))

c = torch.from_numpy(np.array([[1, 2],
                               [2, 3]
                               ]))

print(c)
