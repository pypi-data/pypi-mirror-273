aws s3 sync s3://clay-v1-data/sentinel-2-l2a/S2A_14QKG_20210218_1_L2A/ ~/test/sentinel-2-l2a/S2A_14QKG_20210218_1_L2A/
aws s3 sync s3://clay-v1-data/sentinel-2-l2a/S2A_37WEN_20190330_0_L2A/ ~/test/sentinel-2-l2a/S2A_37WEN_20190330_0_L2A/
aws s3 sync s3://clay-v1-data/sentinel-2-l2a/S2A_51KXT_20200830_0_L2A/ ~/test/sentinel-2-l2a/S2A_51KXT_20200830_0_L2A/
aws s3 sync s3://clay-v1-data/sentinel-2-l2a/S2A_10SEJ_20190331_0_L2A/ ~/test/sentinel-2-l2a/S2A_10SEJ_20190331_0_L2A/

aws s3 sync s3://clay-v1-data/index/sentinel-2-l2a/S2A_14QKG_20210218_1_L2A/ ~/test-index/sentinel-2-l2a/S2A_14QKG_20210218_1_L2A/
aws s3 sync s3://clay-v1-data/index/sentinel-2-l2a/S2A_37WEN_20190330_0_L2A/ ~/test-index/sentinel-2-l2a/S2A_37WEN_20190330_0_L2A/
aws s3 sync s3://clay-v1-data/index/sentinel-2-l2a/S2A_51KXT_20200830_0_L2A/ ~/test-index/sentinel-2-l2a/S2A_51KXT_20200830_0_L2A/
aws s3 sync s3://clay-v1-data/index/sentinel-2-l2a/S2A_10SEJ_20190331_0_L2A/ ~/test-index/sentinel-2-l2a/S2A_10SEJ_20190331_0_L2A/

export GDAL_DISABLE_READDIR_ON_OPEN=YES
export CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif,.png,.jp2"

from pyarrow import dataset as ds
part = ds.partitioning(field_names=["platform", "item"])
data = ds.dataset(
    f"/home/ubuntu/test-index",
    format="parquet",
    partitioning=part,
)
ds.write_dataset(
    data,
    "/home/ubuntu/chipper-index-small",
    format="parquet",
)

/efs/index/


(claymodel) ubuntu@ip-172-31-24-130:~$ s5cmd sync s3://clay-v1-data/* /efs/ &
[1] 9489
