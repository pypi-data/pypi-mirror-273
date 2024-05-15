from lensless import ADMM
import torch
from lensless.utils.image import resize
import matplotlib.pyplot as plt
from datasets import load_dataset
from huggingface_hub import hf_hub_download
import numpy as np
import cv2

repo_id = "Lensless/lensless-optical-1K"

# If the dataset is gated/private, make sure you have run huggingface-cli login
dataset = load_dataset(repo_id, split="test")
psf_fp = hf_hub_download(repo_id=repo_id, filename="psf.tiff", repo_type="dataset")

n_iter = 10
downsample = 6
idx = 10

# get data
h = dataset[idx]
lensless = h["lensless"]
lensed = h["lensed"]
lensless_np = np.array(lensless)
print("Original data range: ", lensless_np.min(), lensless_np.max())
print("Original data shape: ", lensless_np.shape)

# -- prepare data
lensless_np = lensless_np.astype(np.float32)
if downsample != 1:
    lensless_np = resize(lensless_np, factor=1/downsample)
lensless_np = lensless_np / 255
lensless_torch = torch.from_numpy(lensless_np)
lensless_torch = lensless_torch.unsqueeze(0)
print("\nData range: ", lensless_torch.min(), lensless_torch.max())
print("Data shape: ", lensless_torch.shape)

# -- prepare PSF
psf_np = cv2.imread(psf_fp, cv2.IMREAD_UNCHANGED)
psf_np = psf_np.astype(np.float32)
if downsample != 1:
    psf_np = resize(psf_np, factor=1/downsample)
psf_np /= 4095.0
psf_torch = torch.from_numpy(psf_np)
psf_torch = psf_torch.unsqueeze(0)
print("\nPSF range: ", psf_torch.min(), psf_torch.max())
print("PSF shape: ", psf_torch.shape)

# create reconstruction object
recon = ADMM(psf_torch, n_iter=n_iter)

# set data
recon.set_data(lensless_torch)

# reconstruct
res = recon.apply(plot=False)
rec = res[0].numpy()
rec = rec / rec.max()
print("\nReconstruction range: ", rec.min(), rec.max())
print("Reconstruction shape: ", rec.shape)

# plot with two subplots
fig, axs = plt.subplots(1, 3, figsize=(10, 20))
axs[0].imshow(lensless)
axs[1].imshow(rec)
axs[2].imshow(lensed)

# save
plt.savefig("reconstruction.png")