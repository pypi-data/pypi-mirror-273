```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 875815656045.dkr.ecr.us-east-1.amazonaws.com
docker build -t stacchip .
docker tag stacchip:latest 875815656045.dkr.ecr.us-east-1.amazonaws.com/stacchip:latest
docker push 875815656045.dkr.ecr.us-east-1.amazonaws.com/stacchip:latest
```

```python
import geopandas as gp
from pyarrow import dataset as ds
import geoarrow.pyarrow as ga
import geoarrow.pyarrow.dataset as gads

# data = ds.dataset(
#     "/home/tam/Desktop/output",
#     format="parquet",
# )

# 
# dataset = gads.dataset(tab)
dataset = gads.dataset("/home/tam/Desktop/output", format="parquet")
tab = dataset.to_table()

gdf = gp.GeoDataFrame(geometry=ga.to_geopandas(tab["geometry"]))

for col in tab.column_names:
    if col == "geometry":
        continue
    gdf[col] = tab[col].to_numpy()

# bla.crs = "EPSG:32755"
bla.crs = "EPSG:4326"
bla.to_file("/home/tam/Desktop/chip_index_all.fgb")
```


```python
import geoarrow.pyarrow.dataset as gads
from stacchip.chipper import Chipper
import pyarrow as pa
import geopandas as gp
import geoarrow.pyarrow as ga
import numpy as np

# Load a stacchip index table
# dataset = gads.dataset("/home/tam/Desktop/output", format="parquet")
dataset = gads.dataset("/home/tam/Desktop/clay-v1-naip-index/naip/fl_m_3008121_sw_17_1_20171026_20180123/index_fl_m_3008121_sw_17_1_20171026_20180123.parquet", format="parquet")
table = dataset.to_table()

row=42

chipper = Chipper(
    mountpath="/home/tam/Desktop/clay-v1-naip-data",
    platform="naip",
    item_id="fl_m_3008121_sw_17_1_20171026_20180123",
    chip_index_x = table.column("chip_index_x")[row].as_py(),
    chip_index_y = table.column("chip_index_y")[row].as_py()
)
data = chipper.chip

####### Work on validation of row
from matplotlib import pyplot as plt
from PIL import Image

# rgb = np.vstack((
#             data["red"],
#             data["green"],
#             data["blue"],
# )).astype("float32")
# rgb = 255 * rgb / 1000
rgb = np.clip(rgb, 0, 255).astype("uint8").swapaxes(0, 1).swapaxes(1, 2)

rgb = data["image"][:3].swapaxes(0, 1).swapaxes(1, 2)

img = Image.fromarray(rgb, 'RGB')
img.save(f'/home/tam/Desktop/chip_index_row_{row}.png')
# plt.imshow(rgb.astype("uint8"), interpolation='nearest')
# plt.show()

# filtered_table = table.filter(pa.compute.field("item") == table.column("item")[row]).filter(pa.compute.field("chip_index_y") == table.column("chip_index_y")[row]).filter(pa.compute.field("chip_index_x") == table.column("chip_index_x")[row])
filtered_table = table.filter(pa.compute.field("chip_index_y") == table.column("chip_index_y")[row]).filter(pa.compute.field("chip_index_x") == table.column("chip_index_x")[row])

gdf = gp.GeoDataFrame(geometry=ga.to_geopandas(filtered_table["geometry"]))

for col in filtered_table.column_names:
    if col == "geometry":
        continue
    gdf[col] = filtered_table[col].to_numpy()

# bla.crs = "EPSG:32755"
gdf.crs = "EPSG:4326"
gdf.to_file(f"/home/tam/Desktop/chip_index_row_{row}.fgb")
```

```python
filtered_table = table.filter(pa.compute.field("item") == ).filter(pa.compute.field("chip_index_y") == table.column("chip_index_y")[row])
```


## Prechip


```python
os.environ["STACCHIP_TARGETPATH"] = "/home/tam/Desktop/clay-v1-data-small/prechip-tiles"
os.environ["STACCHIP_INDEXPATH"] = "/home/tam/Desktop/clay-v1-data-small/index-combined"
os.environ["STACCHIP_MOUNTPATH"] = "/home/tam/Desktop/clay-v1-data-small"
os.environ["AWS_BATCH_JOB_ARRAY_INDEX"] = "0"
process()

import geoarrow.pyarrow.dataset as gads
import pyarrow as pa

dataset = pa.dataset.dataset("/home/tam/Desktop/clay-v1-data-full-index", format="parquet")
table = dataset.to_table(columns=["chipid", "platform", "chip_index_x", "chip_index_y"])
for platform in ["naip", "linz", "sentinel-2-l2a", "landsat-c2l1", "landsat-c2l2-sr", "sentinel-1-rtc"]:
    filtered_table = table.filter(pa.compute.field("platform") == platform)
    print(f"{platform}: {filtered_table.shape[0]}")


```
import geoarrow.pyarrow.dataset as gads

```bash
/home/tam/Desktop/clay-v1-data-small/

s5cmd sync s3://clay-v1-data/landsat-c2l2-sr/LC08_L2SP_123042_20191207_20200824_02_T1_SR/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l2-sr/LC08_L2SP_123042_20191207_20200824_02_T1_SR/ &
s5cmd sync s3://clay-v1-data/landsat-c2l2-sr/LC08_L2SP_123042_20200312_20200822_02_T2_SR/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l2-sr/LC08_L2SP_123042_20200312_20200822_02_T2_SR/ &
s5cmd sync s3://clay-v1-data/landsat-c2l2-sr/LC09_L2SP_232091_20220217_20230427_02_T1_SR/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l2-sr/LC09_L2SP_232091_20220217_20230427_02_T1_SR/ &
s5cmd sync s3://clay-v1-data/landsat-c2l2-sr/LC09_L2SP_232091_20221031_20230323_02_T1_SR/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l2-sr/LC09_L2SP_232091_20221031_20230323_02_T1_SR/ &
s5cmd sync s3://clay-v1-data/landsat-c2l1/LC08_L1TP_172064_20220325_20220330_02_T1/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l1/LC08_L1TP_172064_20220325_20220330_02_T1/ &
s5cmd sync s3://clay-v1-data/landsat-c2l1/LC08_L1TP_172069_20210306_20210312_02_T1/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l1/LC08_L1TP_172069_20210306_20210312_02_T1/ &
s5cmd sync s3://clay-v1-data/landsat-c2l1/LO09_L1TP_028038_20220316_20230424_02_T1/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l1/LO09_L1TP_028038_20220316_20230424_02_T1/ &
s5cmd sync s3://clay-v1-data/landsat-c2l1/LO09_L1TP_032035_20220312_20230425_02_T1/* /home/tam/Desktop/clay-v1-data-small/landsat-c2l1/LO09_L1TP_032035_20220312_20230425_02_T1/ &
s5cmd sync s3://clay-v1-data/naip/or_m_4512117_sw_10_1_20160804_20160919/* /home/tam/Desktop/clay-v1-data-small/naip/or_m_4512117_sw_10_1_20160804_20160919/ &
s5cmd sync s3://clay-v1-data/naip/wy_m_4310521_se_13_060_20220628/* /home/tam/Desktop/clay-v1-data-small/naip/wy_m_4310521_se_13_060_20220628/ &
s5cmd sync s3://clay-v1-data/linz/CC11_1000_0819/* /home/tam/Desktop/clay-v1-data-small/linz/CC11_1000_0819/ &
s5cmd sync s3://clay-v1-data/linz/CC11_1000_0830/* /home/tam/Desktop/clay-v1-data-small/linz/CC11_1000_0830/ &
s5cmd sync s3://clay-v1-data/sentinel-2-l2a/S2A_16WFB_20220619_0_L2A/* /home/tam/Desktop/clay-v1-data-small/sentinel-2-l2a/S2A_16WFB_20220619_0_L2A/ &
s5cmd sync s3://clay-v1-data/sentinel-2-l2a/S2A_16XDJ_20191005_0_L2A/* /home/tam/Desktop/clay-v1-data-small/sentinel-2-l2a/S2A_16XDJ_20191005_0_L2A/ &

s5cmd sync s3://clay-v1-data/index/landsat-c2l2-sr/LC08_L2SP_123042_20191207_20200824_02_T1_SR/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l2-sr/LC08_L2SP_123042_20191207_20200824_02_T1_SR/ &
s5cmd sync s3://clay-v1-data/index/landsat-c2l2-sr/LC08_L2SP_123042_20200312_20200822_02_T2_SR/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l2-sr/LC08_L2SP_123042_20200312_20200822_02_T2_SR/ &
s5cmd sync s3://clay-v1-data/index/landsat-c2l2-sr/LC09_L2SP_232091_20220217_20230427_02_T1_SR/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l2-sr/LC09_L2SP_232091_20220217_20230427_02_T1_SR/ &
s5cmd sync s3://clay-v1-data/index/landsat-c2l2-sr/LC09_L2SP_232091_20221031_20230323_02_T1_SR/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l2-sr/LC09_L2SP_232091_20221031_20230323_02_T1_SR/ &
s5cmd sync s3://clay-v1-data/index/landsat-c2l1/LC08_L1TP_172064_20220325_20220330_02_T1/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l1/LC08_L1TP_172064_20220325_20220330_02_T1/ &
s5cmd sync s3://clay-v1-data/index/landsat-c2l1/LC08_L1TP_172069_20210306_20210312_02_T1/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l1/LC08_L1TP_172069_20210306_20210312_02_T1/ &
s5cmd sync s3://clay-v1-data/index/landsat-c2l1/LO09_L1TP_028038_20220316_20230424_02_T1/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l1/LO09_L1TP_028038_20220316_20230424_02_T1/ &
s5cmd sync s3://clay-v1-data/index/landsat-c2l1/LO09_L1TP_032035_20220312_20230425_02_T1/* /home/tam/Desktop/clay-v1-data-small/index/landsat-c2l1/LO09_L1TP_032035_20220312_20230425_02_T1/ &
s5cmd sync s3://clay-v1-data/index/naip/or_m_4512117_sw_10_1_20160804_20160919/* /home/tam/Desktop/clay-v1-data-small/index/naip/or_m_4512117_sw_10_1_20160804_20160919/ &
s5cmd sync s3://clay-v1-data/index/naip/wy_m_4310521_se_13_060_20220628/* /home/tam/Desktop/clay-v1-data-small/index/naip/wy_m_4310521_se_13_060_20220628/ &
s5cmd sync s3://clay-v1-data/index/linz/CC11_1000_0819/* /home/tam/Desktop/clay-v1-data-small/index/linz/CC11_1000_0819/ &
s5cmd sync s3://clay-v1-data/index/linz/CC11_1000_0830/* /home/tam/Desktop/clay-v1-data-small/index/linz/CC11_1000_0830/ &
s5cmd sync s3://clay-v1-data/index/sentinel-2-l2a/S2A_16WFB_20220619_0_L2A/* /home/tam/Desktop/clay-v1-data-small/index/sentinel-2-l2a/S2A_16WFB_20220619_0_L2A/ &
s5cmd sync s3://clay-v1-data/index/sentinel-2-l2a/S2A_16XDJ_20191005_0_L2A/* /home/tam/Desktop/clay-v1-data-small/index/sentinel-2-l2a/S2A_16XDJ_20191005_0_L2A/ &




AWS_BATCH_JOB_ARRAY_INDEX=0 \
    STACCHIP_DATA_BUCKET=clay-v1-data \
    STACCHIP_CHIP_BUCKET=clay-v1-data-chips \
    STACCHIP_PLATFORM=naip \
    STACCHIP_INDEXPATH=/home/tam/Desktop/clay-v1-data-full-index \
    stacchip-prechip


os.environ["AWS_BATCH_JOB_ARRAY_INDEX"] = "0"
os.environ["STACCHIP_BUCKET"] = "clay-v1-data"
process()




os.environ["AWS_BATCH_JOB_ARRAY_INDEX"] = "0"
os.environ["STACCHIP_DATA_BUCKET"] = "clay-v1-data"
os.environ["STACCHIP_INDEXPATH"] = "/home/tam/Desktop/clay-v1-data-full-index/"
os.environ["STACCHIP_CHIP_BUCKET"] = "clay-v1-data-chips"
os.environ["STACCHIP_PLATFORM"] = "linz"
os.environ["STACCHIP_CUBES_PER_JOB"] = "100"
os.environ["STACCHIP_POOL_SIZE"] = "24"
process()




os.environ["AWS_BATCH_JOB_ARRAY_INDEX"] = "0"
os.environ["STACCHIP_BUCKET"] = "clay-v1-data"
os.environ["STACCHIP_MGRS_SOURCE"] = (
    "https://clay-mgrs-samples.s3.amazonaws.com/mgrs_sample_v02.fgb"
)

process()
```


```python


import geoarrow.pyarrow.dataset as gads
from stacchip.chipper import Chipper
import pyarrow as pa
import geopandas as gp
import geoarrow.pyarrow as ga
import numpy as np

# Load a stacchip index table
# dataset = gads.dataset("/home/tam/Desktop/output", format="parquet")
part =  ds.partitioning(field_names=["item_id"])
dataset = gads.dataset("/home/tam/Desktop/clay-v1-naip-index/naip/fl_m_3008121_sw_17_1_20171026_20180123/index_fl_m_3008121_sw_17_1_20171026_20180123.parquet", format="parquet")
table = dataset.to_table()
```