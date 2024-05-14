from ..controller.meta_data_extractor import MetadataExtractor
from ..controller.metadata_model import MetadataModel


class TestMetaDataExtractor:
    def test_entry_values_computer(self):
        obj = MetadataModel(
            filename="20161101_091032002000000_TCX8020.tif",
            region="091032002000000",
            fileuri="s3://satimg-to-be-deleted/Sentinel2/TCX8020/20161101_091032002000000_TCX8020.tif",
            product="TCX8020",
            date="20161101",
            date_region_product="20161101_091032002000000_TCX8020",
            pixelsize="10.0 -10.0",
            # crs=crs,
            upperleft="415320.0 2016620.0",
            lowerleft="415320.0 1900630.0",
            lowerright="533630.0 1900630.0",
            upperright="533630.0 2016620.0",
            nodata="0.0",
            width="11831",
            height="11599",
            datatype="Byte",
            max="193",
            min="50",
            mean="155.31843492351",
            stddev="16.361398072633",
            valid_perc="50.82",
            origin="415320.0 2016620.0",
            filesize_mb="56.69",
            compression="LZW",
        )

        result = MetadataExtractor(None, None)._entry_values_computer(obj)
        print(result)
