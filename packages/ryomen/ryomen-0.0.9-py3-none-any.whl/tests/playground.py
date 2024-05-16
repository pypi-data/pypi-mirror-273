from ryomen.main import Slicer
import numpy as np
import torch
import zarr
from tqdm import tqdm


s = 8
N = 3
leading_dims=1
image = np.arange(3000 * 2000 * 50).reshape((3000, 2000, 50))
print('generated')
# image = zarr.zeros(([1] * leading_dims) + ([s, ] * N))
# image[:] = _image
output = zarr.zeros(shape=(3000, 2000, 50))
crop = (512, 512, 10)
overlap = (10, 10, 2)
crop_iterator = Slicer(
    image, crop_size=crop, overlap=overlap, batch_size=1, pad=True,
)
print(len(crop_iterator))
for crop, source, destination in tqdm(crop_iterator):
    output[destination] = crop[source]
#
# #
# # print(np.min(((image * 100) - 3) - output))
# # assert np.allclose((image * 100) - 3, output)
assert np.allclose(image[:], output), f'\n\n{image-output}'
#
