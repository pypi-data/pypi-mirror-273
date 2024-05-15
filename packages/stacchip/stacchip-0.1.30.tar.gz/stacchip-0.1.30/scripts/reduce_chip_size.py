from multiprocessing import Pool
from pathlib import Path

import numpy as np

src = Path("/home/tam/Desktop/clay-v1-data-chips-naip")

paths = [path for path in src.glob("**/*.npz")]


def process(path):
    print(path)
    data = dict(np.load(path))
    data["pixels"] = data["pixels"][:, :224, :224]
    counter = path.stem.split("_")[1]
    np.savez_compressed(
        f"/home/tam/Desktop/clay-v1-data-chips-naip-224/chip_{counter}.npz",
        data["pixels"],
        data["lon_norm"],
        data["lat_norm"],
        data["week_norm"],
        data["hour_norm"],
    )


with Pool(12) as p:
    p.map(process, paths)
