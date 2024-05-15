from huggingface_hub import hf_hub_download
import matplotlib.pyplot as plt
from lensless.utils.io import load_image, load_psf
from lensless.recon.admm import apply_admm
from lensless.recon.gd import apply_gradient_descent
from lensless.recon.rfft_convolve import RealFFTConvolve2D
import numpy as np


repo_id = "bezzam/DiffuserCam-Lensless-Mirflickr-Dataset-NORM"
psf = "psf.tiff"
lensless = "lensless_example.png"
lensed = "lensed_example.png"

n_iter = 10
downsample = 4
use_torch = True
flip_ud = True

# download individual files
psf_fp = hf_hub_download(repo_id=repo_id, filename=psf, repo_type="dataset")
lensless_fp = hf_hub_download(repo_id=repo_id, filename=lensless, repo_type="dataset")
lensed_fp = hf_hub_download(repo_id=repo_id, filename=lensed, repo_type="dataset")

# apply ADMM
print("\n-- ADMM")
res = apply_admm(psf_fp, lensless_fp, n_iter, downsample=downsample, use_torch=use_torch, flip_ud=flip_ud, verbose=True)
if use_torch:
    res = res.cpu().numpy()
res_admm = res[0] / res.max()

# apply GD
print("\n-- Gradient descent")
# res_gd = apply_gradient_descent(psf_fp, lensless_fp, n_iter=300, proj=lambda x:x, downsample=downsample, use_torch=use_torch, flip_ud=flip_ud, verbose=True)
res_gd = apply_gradient_descent(psf_fp, lensless_fp, n_iter=300, downsample=downsample, use_torch=use_torch, flip_ud=flip_ud, verbose=True)
if use_torch:
    res_gd = res_gd.cpu().numpy()
res_gd = res_gd[0] / res_gd.max()

# linear reconstruction with just adjoint
psf = load_psf(psf_fp, downsample=downsample, flip_ud=flip_ud)
lensless_img  = load_image(lensless_fp, downsample=downsample / 4, flip_ud=flip_ud, as_4d=True)
physics = RealFFTConvolve2D(psf=psf)
K = 1e-4
physics._Hadj = physics._Hadj / (np.linalg.norm(physics._H) ** 2 + K)
res_inv = physics.deconvolve(lensless_img).squeeze()
res_inv = res_inv / res_inv.max()

# plot lensless, reconstruction, and ground truth
# -- measurements already 4x downsampled wrt to PSF
lensed_img = load_image(lensed_fp, downsample=downsample / 4, flip_ud=flip_ud)

fig, ax = plt.subplots(1, 5, figsize=(15, 5))
ax[0].imshow(lensless_img[0])
ax[0].set_title("Raw")
ax[1].imshow(res_inv)
ax[1].set_title("Adjoint")
ax[2].imshow(res_gd)
ax[2].set_title("GD")
ax[3].imshow(res_admm)
ax[3].set_title("ADMM")
ax[4].imshow(lensed_img)
ax[4].set_title("Lensed")

plt.show()
