import os
import shutil
from glob import glob

import numpy as np
from csbdeep.utils import normalize
from skimage import img_as_uint, io
from stardist.models import StarDist2D
from tqdm import tqdm

# initialize directory constants, change to fit your data
# DATA_DIR is source data
# OUTPUT_DIR is where single-file time series will be saved
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

if __name__ == "__main__":
    # clean the output directory to avoid confusion
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR)

    # load pretrained model
    model = StarDist2D.from_pretrained("2D_versatile_fluo")

    # loop through all image paths in the data directory
    img_paths = sorted(glob(os.path.join(DATA_DIR, "*.tif")))

    for p in img_paths:
        img = io.imread(p)

        # check number of dimensions, and that frame dimension is the first
        assert img.ndim == 3
        assert img.shape[0] < img.shape[1]

        # initiate a list
        frame_labels = []

        # iterate through frames along axis 0
        print(f"Predicting frames for {os.path.basename(p)}")
        for f in tqdm(range(img.shape[0])):
            frame = img[f]
            labels, _ = model.predict_instances(normalize(frame))

            # append 16-bit uint to list
            # remove call to img_as_uint if you want 32-bit float dtype
            frame_labels.append(img_as_uint(labels))

        # convert list of np.ndarrays to np.ndarray
        frame_labels = np.array(frame_labels)

        io.imsave(
            os.path.join(OUTPUT_DIR, os.path.basename(p)),
            frame_labels,
            check_contrast=False,
        )
