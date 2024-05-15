import gzip
import io

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from fastavro import reader, writer
from scipy import ndimage


def make_triplet(alert, normalize: bool = False) -> np.ndarray:
    """
    Make stacked triplet from alert packet

    Parameters:
    ----------
    alert : dict
        Alert packet
    normalize: bool
        Normalize the cutout counts; False by default

    Returns:
    ----------
    triplet: np.ndarray
        Stacked triplet of science, reference and difference cutouts
    """
    cutout_dict = dict()

    for cutout in ["science", "template", "difference"]:
        cutout_zipped = alert["cutout_" + cutout]

        with gzip.open(io.BytesIO(cutout_zipped), "rb") as f:
            with fits.open(io.BytesIO(f.read())) as hdu:
                cut_data = hdu[0].data
                cutout_dict[cutout] = np.nan_to_num(cut_data)
                if normalize:
                    cutout_dict[cutout] /= np.linalg.norm(cutout_dict[cutout])
                    cutout_dict[cutout] -= np.nanmean(cutout_dict[cutout])

    shape = np.shape(cutout_dict[cutout]) + (3,)
    triplet = np.zeros(shape)
    triplet[:, :, 0] = cutout_dict["science"]
    triplet[:, :, 1] = cutout_dict["template"]
    triplet[:, :, 2] = cutout_dict["difference"]

    return triplet


def pick_alert(avro_path: str, candid: int, write_alert: bool = False) -> list:
    """
    Pick out specific alert packet from combined avro file

    Parameters:
    ----------
    avro_path : str
        Path to avro file
    candid: int
        Candidate ID; unique identifier

    Returns:
    ----------
    candidate_record: list
        alert packet
    """
    candidate_record = []
    with open(avro_path, "rb") as avro_f:
        avro_reader = reader(avro_f)
        schema = avro_reader.writer_schema
        for record in avro_reader:
            if record["candid"] == candid:
                candidate_record.append(record)
                if write_alert:
                    with open(str(candid) + ".avro", "wb") as out:
                        writer(out, schema, candidate_record)

    return candidate_record


def rotate_triplet(triplet):
    """
    Rotate the triplet by 90, 180 and 270 degrees

    Args:
        triplet: Triplet of cutouts

    Returns:

    """
    sci, ref, diff = triplet[:, :, 0], triplet[:, :, 1], triplet[:, :, 2]
    trip90 = np.stack(
        (ndimage.rotate(sci, 90), ndimage.rotate(ref, 90), ndimage.rotate(diff, 90)),
        axis=-1,
    )
    trip180 = np.stack(
        (ndimage.rotate(sci, 180), ndimage.rotate(ref, 180), ndimage.rotate(diff, 180)),
        axis=-1,
    )
    trip270 = np.stack(
        (ndimage.rotate(sci, 270), ndimage.rotate(ref, 270), ndimage.rotate(diff, 270)),
        axis=-1,
    )
    return trip90, trip180, trip270


def plot_triplet(stack: np.ndarray, pdf: bool = False) -> None:
    """
    Plot cutouts of sci, ref and diff from stacked triplet

    Parameters:
    ----------
    stack: np.ndarray
        Stack of cutouts
    pdf: bool
        Save plots in a pdf file

    Returns:
    ----------
    None
    """

    # read cutouts
    sci, ref, diff = stack[:, :, 0], stack[:, :, 1], stack[:, :, 2]

    # plot cutouts
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    _, median, std = sigma_clipped_stats(sci)
    ax[0].imshow(sci, vmin=median - 5 * std, vmax=median + 5 * std, origin="lower")
    ax[0].set_title("sci")
    ax[0].axis("off")
    _, median, std = sigma_clipped_stats(ref)
    ax[1].imshow(ref, vmin=median - 5 * std, vmax=median + 5 * std, origin="lower")
    ax[1].set_title("ref")
    ax[1].axis("off")
    _, median, std = sigma_clipped_stats(diff)
    ax[2].imshow(diff, vmin=median - 5 * std, vmax=median + 5 * std, origin="lower")
    ax[2].set_title("diff")
    ax[2].axis("off")

    # save to pdf if necessary
    if pdf:
        pdf.savefig()
        plt.close()
    else:
        plt.show()
