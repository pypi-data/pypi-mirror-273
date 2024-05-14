from dataclasses import dataclass


@dataclass
class MetadataModel:
    filename: str
    region: str
    product: str
    date: str
    date_region_product: str
    fileuri: str
    pixelsize: str
    # crs: str
    upperleft: str
    lowerleft: str
    lowerright: str
    upperright: str
    nodata: str
    width: str
    height: str
    datatype: str
    max: str
    min: str
    mean: str
    stddev: str
    valid_perc: str
    origin: str
    filesize_mb: str
    compression: str
    metadata_check: str = ""


class QaQcModel:
    filename_parts_count: str
    filename_endswith: str
    filename_date_chars: int
    filename_product_code: list
    filename_product_code_count: int
    filename_season_code_count: int
    filename_season_code_startswith: str
    # epsg_code_count: int
    pixelsize: str
    nodata_value: str
    values_range: list
    compression_type: str
