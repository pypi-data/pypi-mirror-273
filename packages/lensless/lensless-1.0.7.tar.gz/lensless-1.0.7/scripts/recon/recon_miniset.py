from datasets import load_dataset
from huggingface_hub import hf_hub_download
import numpy as np
from lensless.utils.io import load_psf

repo_id = "Lensless/lensless-mini"
downsample = 4

# If the dataset is gated/private, make sure you have run huggingface-cli login
dataset = load_dataset(repo_id, split="all")
psf_fp = hf_hub_download(repo_id=repo_id, filename="psf.tiff", repo_type="dataset")


# load PSF
psf, bg = load_psf(
    psf_fp,
    verbose=False,
    downsample=downsample,
    return_bg=True,
    flip_ud=False,
    dtype="float32",
    bg_pix=(0, 15),
)



# loop over dataset
for i in range(len(dataset)):
    lensless = dataset[i]["lensless"]
    lensed = dataset[i]["lensed"]

    # to numpy
    lensless_np = np.array(lensless)
    lensed_np = np.array(lensed)



import pudb; pudb.set_trace()