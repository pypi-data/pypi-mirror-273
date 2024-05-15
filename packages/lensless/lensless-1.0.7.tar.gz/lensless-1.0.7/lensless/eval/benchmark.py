# #############################################################################
# benchmark.py
# =================
# Authors :
# Yohann PERRON
# Eric BEZZAM [ebezzam@gmail.com]
# #############################################################################


from lensless.utils.dataset import DiffuserCamTestDataset
from lensless.utils.io import save_image
from waveprop.noise import add_shot_noise
from tqdm import tqdm
import os
import numpy as np
import wandb

try:
    import torch
    from torch.utils.data import DataLoader
    from torch.nn import MSELoss, L1Loss
    from torchmetrics import StructuralSimilarityIndexMeasure
    from torchmetrics.image import lpip, psnr
except ImportError:
    raise ImportError(
        "Torch, torchvision, and torchmetrics are needed to benchmark reconstruction algorithm."
    )


def benchmark(
    model,
    dataset,
    batchsize=1,
    metrics=None,
    crop=None,
    save_idx=None,
    output_dir=None,
    unrolled_output_factor=False,
    return_average=True,
    snr=None,
    use_wandb=False,
    label=None,
    epoch=None,
    **kwargs,
):
    """
    Compute multiple metrics for a reconstruction algorithm.

    Parameters
    ----------
    model : :py:class:`~lensless.ReconstructionAlgorithm`
        Reconstruction algorithm to benchmark.
    dataset : :py:class:`~lensless.benchmark.ParallelDataset`
        Parallel dataset of lensless and lensed images.
    batchsize : int, optional
        Batch size for processing. For maximum compatibility use 1 (batchsize above 1 are not supported on all algorithm), by default 1
    metrics : dict, optional
        Dictionary of metrics to compute. If None, MSE, MAE, SSIM, LPIPS and PSNR are computed.
    save_idx : list of int, optional
        List of indices to save the predictions, by default None (not to save any).
    output_dir : str, optional
        Directory to save the predictions, by default save in working directory if save_idx is provided.
    crop : dict, optional
        Dictionary of crop parameters (vertical: [start, end], horizontal: [start, end]), by default None (no crop).
    unrolled_output_factor : bool, optional
        If True, compute metrics for unrolled output, by default False.
    return_average : bool, optional
        If True, return the average value of the metrics, by default True.
    snr : float, optional
        Signal to noise ratio for adding shot noise. If None, no noise is added, by default None.

    Returns
    -------
    Dict[str, float]
        A dictionnary containing the metrics name and average value
    """
    assert isinstance(model._psf, torch.Tensor), "model need to be constructed with torch support"
    device = model._psf.device

    if output_dir is None:
        output_dir = os.getcwd()
    else:
        output_dir = str(output_dir)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    if metrics is None:
        metrics = {
            "MSE": MSELoss().to(device),
            # "MAE": L1Loss().to(device),
            "LPIPS_Vgg": lpip.LearnedPerceptualImagePatchSimilarity(
                net_type="vgg", normalize=True
            ).to(device),
            # "LPIPS_Alex": lpip.LearnedPerceptualImagePatchSimilarity(
            #     net_type="alex", normalize=True
            # ).to(device),
            "PSNR": psnr.PeakSignalNoiseRatio().to(device),
            "SSIM": StructuralSimilarityIndexMeasure().to(device),
            "ReconstructionError": None,
        }

    metrics_values = {key: [] for key in metrics}
    if unrolled_output_factor:
        output_metrics = metrics.keys()
        for key in output_metrics:
            if key != "ReconstructionError":
                metrics_values[key + "_unrolled"] = []

    # loop over batches
    dataloader = DataLoader(dataset, batch_size=batchsize, pin_memory=(device != "cpu"))
    model.reset()
    idx = 0
    with torch.no_grad():
        for batch in tqdm(dataloader):
            if hasattr(dataset, "multimask"):
                if dataset.multimask:
                    lensless, lensed, psfs = batch
                    psfs = psfs.to(device)
                else:
                    lensless, lensed = batch
                    psfs = None
            else:
                lensless, lensed = batch
                psfs = None

            lensless = lensless.to(device)
            lensed = lensed.to(device)

            # add shot noise
            if snr is not None:
                for i in range(lensless.shape[0]):
                    lensless[i] = add_shot_noise(lensless[i], float(snr))

            # compute predictions
            if batchsize == 1:
                if psfs is not None:
                    model._set_psf(psfs[0])
                model.set_data(lensless)
                prediction = model.apply(
                    plot=False, save=False, output_intermediate=unrolled_output_factor, **kwargs
                )

            else:
                prediction = model.forward(lensless, psfs, **kwargs)

            if unrolled_output_factor:
                unrolled_out = prediction[-1]
                prediction = prediction[0]
            prediction_original = prediction.clone()

            # Convert to [N*D, C, H, W] for torchmetrics
            prediction = prediction.reshape(-1, *prediction.shape[-3:]).movedim(-1, -3)
            lensed = lensed.reshape(-1, *lensed.shape[-3:]).movedim(-1, -3)

            if hasattr(dataset, "alignment"):
                if dataset.alignment is not None:
                    prediction = dataset.extract_roi(prediction, axis=(-2, -1))
                else:
                    prediction, lensed = dataset.extract_roi(
                        prediction, axis=(-2, -1), lensed=lensed
                    )
                assert np.all(lensed.shape == prediction.shape)
            elif crop is not None:
                prediction = prediction[
                    ...,
                    crop["vertical"][0] : crop["vertical"][1],
                    crop["horizontal"][0] : crop["horizontal"][1],
                ]
                lensed = lensed[
                    ...,
                    crop["vertical"][0] : crop["vertical"][1],
                    crop["horizontal"][0] : crop["horizontal"][1],
                ]

            if save_idx is not None:
                batch_idx = np.arange(idx, idx + batchsize)

                for i, _batch_idx in enumerate(batch_idx):
                    if _batch_idx in save_idx:
                        prediction_np = prediction.cpu().numpy()[i]
                        # switch to [H, W, C] for saving
                        prediction_np = np.moveaxis(prediction_np, 0, -1)
                        fp = os.path.join(output_dir, f"{_batch_idx}.png")
                        save_image(prediction_np, fp=fp)

                        if use_wandb:
                            assert epoch is not None, "epoch must be provided for wandb logging"
                            log_key = (
                                f"{_batch_idx}_{label}" if label is not None else f"{_batch_idx}"
                            )
                            wandb.log({log_key: wandb.Image(fp)}, step=epoch)

            # normalization
            prediction_max = torch.amax(prediction, dim=(-1, -2, -3), keepdim=True)
            if torch.all(prediction_max != 0):
                prediction = prediction / prediction_max
            else:
                print("Warning: prediction is zero")
            lensed_max = torch.amax(lensed, dim=(1, 2, 3), keepdim=True)
            lensed = lensed / lensed_max

            # compute metrics
            for metric in metrics:
                if metric == "ReconstructionError":
                    metrics_values[metric].append(
                        model.reconstruction_error(
                            prediction=prediction_original, lensless=lensless
                        )
                        .cpu()
                        .item()
                    )
                else:
                    try:
                        if "LPIPS" in metric:
                            if prediction.shape[1] == 1:
                                # LPIPS needs 3 channels
                                metrics_values[metric].append(
                                    metrics[metric](
                                        prediction.repeat(1, 3, 1, 1), lensed.repeat(1, 3, 1, 1)
                                    )
                                    .cpu()
                                    .item()
                                )
                            else:
                                metrics_values[metric].append(
                                    metrics[metric](prediction, lensed).cpu().item()
                                )
                        else:
                            metrics_values[metric].append(
                                metrics[metric](prediction, lensed).cpu().item()
                            )
                    except Exception as e:
                        print(f"Error in metric {metric}: {e}")

            # compute metrics for unrolled output
            if unrolled_output_factor:

                # -- convert to CHW and remove depth
                unrolled_out = unrolled_out.reshape(-1, *unrolled_out.shape[-3:]).movedim(-1, -3)

                # -- extraction region of interest
                if crop is not None:
                    unrolled_out = unrolled_out[
                        ...,
                        crop["vertical"][0] : crop["vertical"][1],
                        crop["horizontal"][0] : crop["horizontal"][1],
                    ]

                # -- normalization
                unrolled_out_max = torch.amax(unrolled_out, dim=(-1, -2, -3), keepdim=True)
                if torch.all(unrolled_out_max != 0):
                    unrolled_out = unrolled_out / unrolled_out_max

                # -- compute metrics
                for metric in metrics:
                    if metric == "ReconstructionError":
                        # only have this for final output
                        continue
                    else:
                        if "LPIPS" in metric:
                            if unrolled_out.shape[1] == 1:
                                # LPIPS needs 3 channels
                                metrics_values[metric].append(
                                    metrics[metric](
                                        unrolled_out.repeat(1, 3, 1, 1), lensed.repeat(1, 3, 1, 1)
                                    )
                                    .cpu()
                                    .item()
                                )
                            else:
                                metrics_values[metric + "_unrolled"].append(
                                    metrics[metric](unrolled_out, lensed).cpu().item()
                                )
                        else:
                            metrics_values[metric + "_unrolled"].append(
                                metrics[metric](unrolled_out, lensed).cpu().item()
                            )

            model.reset()
            idx += batchsize

    # average metrics
    if return_average:
        for metric in metrics:
            metrics_values[metric] = np.mean(metrics_values[metric])

    return metrics_values


if __name__ == "__main__":
    from lensless import ADMM

    downsample = 1.0
    batchsize = 1
    n_files = 10
    n_iter = 100

    # check if GPU is available
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    # prepare dataset
    dataset = DiffuserCamTestDataset(n_files=n_files, downsample=downsample)

    # prepare model
    psf = dataset.psf.to(device)
    model = ADMM(psf, n_iter=n_iter)

    # run benchmark
    print(benchmark(model, dataset, batchsize=batchsize))
