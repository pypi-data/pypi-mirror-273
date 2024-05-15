with open("/home/tam/Desktop/all_naip_tiffs.txt") as src:
    paths = src.readlines()

from multiprocessing import Pool
from urllib.parse import urlparse

import rasterio


def drop(path):
    with rasterio.open(path) as rst:
        if rst.count != 4:
            url = urlparse(path)
            print(url)

            item_id = url.path.split("/")[2]
            print("Deleting", item_id)

            s3client = boto3.client("s3")
            s3client.delete_object(Bucket=url.netloc, Key=url.path.lstrip("/"))
            s3client.delete_object(
                Bucket=url.netloc, Key=f"naip/{item_id}/stac_item.json"
            )
            s3client.delete_object(
                Bucket=url.netloc, Key=f"index/naip/{item_id}/index_{item_id}.parquet"
            )
            # print(url.path.lstrip("/"))
            # print(f"index/naip/{item_id}/")
            # print(f"naip/{item_id}/{item_id}.parquet")
            return True


with Pool(24) as p:
    counts = p.map(drop, paths)
