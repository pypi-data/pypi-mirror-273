from os import environ, getenv
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
from metadata_model import MetadataModel
from osgeo import gdal

gdal.UseExceptions()
gdal.SetConfigOption("AWS_DEFAULT_REGION", "ap-south-1")
gdal.SetConfigOption(
    "AWS_SECRET_ACCESS_KEY", "O532YGW4+gYA3Y+NhXiI5w6+MjNdyasgdbpE4490"
)
gdal.SetConfigOption("AWS_ACCESS_KEY_ID", "AKIAVMZ7IZCPHXL6UY4G")
gdal.SetConfigOption("AWS_REQUEST_PAYER", "REQUESTER")

environ["AWS_ACCESS_KEY_ID"] = "AKIAVMZ7IZCPHXL6UY4G"
environ["AWS_SECRET_ACCESS_KEY"] = "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"
environ["AWS_DEFAULT_REGION"] = "ap-south-1"
environ["AWS_REQUEST_PAYER"] = "REQUESTER"


class MetaData:
    def __init__(self, file: str):
        self.file = file

    def main(self) -> MetadataModel:
        """
        Extract metadata from the specified S3 file.
        Returns:
            MetadataModel: Extracted metadata.
        """
        parse_s3_uri = urlparse(self.file, allow_fragments=False)
        bucket_name = parse_s3_uri.netloc
        file_path = parse_s3_uri.path

        # Fetch file stats using GDAL
        info_options = gdal.InfoOptions(stats=True, format="json", computeMinMax=True)
        stats_json = gdal.Info(f"/vsis3/{bucket_name}{file_path}", options=info_options)

        # Get object metadata from S3
        try:
            s3_client = boto3.client("s3")
            response = s3_client.head_object(
                Bucket=bucket_name, Key=file_path[1:], RequestPayer="requester"
            )
            content_length_mb = response["ContentLength"] / (1024 * 1024)
        except ClientError as e:
            raise RuntimeError(f"Error fetching S3 object metadata: {e}")
        # Extract metadata values
        file_parts = self.file.split("/")
        filename = file_parts[-1]
        region = file_parts[-1].split("_")[1]
        product = file_parts[-1].split("_")[2].split(".")[0]
        date = file_parts[-1].split("_")[0]
        date_region_product = f"{date}_{region}_{product}"
        geo_transform = stats_json["geoTransform"]
        # crs = f'EPSG:{stats_json["stac"]["proj:epsg"]}'
        coords = stats_json["cornerCoordinates"]
        upperleft = f'{coords["upperLeft"][0]} {coords["upperLeft"][1]}'
        lowerleft = f'{coords["lowerLeft"][0]} {coords["lowerLeft"][1]}'
        lowerright = f'{coords["lowerRight"][0]} {coords["lowerRight"][1]}'
        upperright = f'{coords["upperRight"][0]} {coords["upperRight"][1]}'
        nodata = str(stats_json["bands"][0]["noDataValue"])
        width = str(stats_json["size"][0])
        height = str(stats_json["size"][1])
        data_type = stats_json["bands"][0]["type"]
        metadata = stats_json["bands"][0]["metadata"][""]
        max_val = metadata.get("STATISTICS_MAXIMUM", "")
        min_val = metadata.get("STATISTICS_MINIMUM", "")
        mean_val = metadata.get("STATISTICS_MEAN", "")
        stddev_val = metadata.get("STATISTICS_STDDEV", "")
        valid_perc = metadata.get("STATISTICS_VALID_PERCENT", "")
        origin = f"{geo_transform[0]} {geo_transform[3]}"
        filesize_mb = str(round(content_length_mb, 2))
        compression = (
            stats_json["metadata"].get("IMAGE_STRUCTURE", {}).get("COMPRESSION", "")
        )

        # Creating MetadataModel object
        new_data = MetadataModel(
            filename=filename,
            region=region,
            fileuri=self.file,
            product=product,
            date=date,
            date_region_product=date_region_product,
            pixelsize=f"{geo_transform[1]} {geo_transform[-1]}",
            # crs=crs,
            upperleft=upperleft,
            lowerleft=lowerleft,
            lowerright=lowerright,
            upperright=upperright,
            nodata=nodata,
            width=width,
            height=height,
            datatype=data_type,
            max=max_val,
            min=min_val,
            mean=mean_val,
            stddev=stddev_val,
            valid_perc=valid_perc,
            origin=origin,
            filesize_mb=filesize_mb,
            compression=compression,
        )

        return new_data
