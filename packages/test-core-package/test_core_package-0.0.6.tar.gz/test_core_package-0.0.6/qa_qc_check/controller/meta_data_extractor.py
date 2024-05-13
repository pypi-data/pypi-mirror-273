import json
import logging
from dataclasses import asdict
from typing import Dict

from qa_qc_check.controller.meta_data import MetaData
from qa_qc_check.controller.metadata_model import MetadataModel, QaQcModel
from qa_qc_check.controller.qa_qc import QaQc

logger = logging.getLogger()


class MetadataExtractor:

    def __init__(self, file: str, check_type: str):
        """Initializing MetadataExtractor

        Args:
            file (str): S3 File Path
            check_type (str): QA/QC check type
        """
        self.file = file
        self.check_type = check_type
        # self.checks_json = json.load(open("checks.json", "r"))
        self.checks_json = {
            "ndvi": {
                "entry": {},
                "exit": {
                    "filename_parts_count": 3,
                    "filename_endswith": ".tif",
                    "filename_date_chars": 8,
                    "filename_product_code": [
                        "TCX8021",
                        "IS18021",
                        "TCX8020",
                        "IS18020",
                    ],
                    "filename_product_code_count": 7,
                    "filename_season_code_count": 0,
                    "filename_season_code_startswith": [""],
                    "epsg_code_count": 5,
                    "pixelsize": "10.0 -10.0",
                    "nodata_value": "0.0",
                    "values_range": [0, 200],
                    "compression_type": "LZW",
                },
                "product_list": ["TCX8021", "IS18021", "TCX8020", "IS18020"],
                "s3_bucket_names": ["satsure-satimg", "satimg-to-be-deleted"],
            },
            "ndwi": {
                "entry": {},
                "exit": {
                    "filename_parts_count": 3,
                    "filename_endswith": ".tif",
                    "filename_date_chars": 8,
                    "filename_product_code": [
                        "TCX9021",
                        "IS19021",
                        "TCX9020",
                        "IS19020",
                    ],
                    "filename_product_code_count": 7,
                    "filename_season_code_count": 0,
                    "filename_season_code_startswith": [""],
                    "pixelsize": "10.0 -10.0",
                    "nodata_value": "0.0",
                    "values_range": [0, 200],
                    "compression_type": "LZW",
                },
                "product_list": ["TCX9021", "IS19021", "TCX9020", "IS19020"],
                "s3_bucket_names": ["satsure-satimg", "satimg-to-be-deleted"],
            },
            "mndwi": {
                "entry": {},
                "exit": {
                    "filename_parts_count": 3,
                    "filename_endswith": ".tif",
                    "filename_date_chars": 8,
                    "filename_product_code": [
                        "TCXD021",
                        "IS1D021",
                        "TCXD020",
                        "IS1D020",
                    ],
                    "filename_product_code_count": 7,
                    "filename_season_code_count": 0,
                    "filename_season_code_startswith": [""],
                    "epsg_code_count": 5,
                    "pixelsize": "10.0 -10.0",
                    "nodata_value": "0.0",
                    "values_range": [0, 200],
                    "compression_type": "LZW",
                },
                "product_list": ["TCXD021", "IS1D021", "TCXD020", "IS1D020"],
                "s3_bucket_names": ["satsure-satimg", "satimg-to-be-deleted"],
            },
            "fcc": {
                "entry": {},
                "exit": {
                    "filename_parts_count": 3,
                    "filename_endswith": ".tif",
                    "filename_date_chars": 8,
                    "filename_product_code": ["IS51010", "IS51011"],
                    "filename_product_code_count": 7,
                    "filename_season_code_count": 0,
                    "filename_season_code_startswith": [""],
                    "epsg_code_count": 5,
                    "pixelsize": "10.0 -10.0",
                    "nodata_value": "0.0",
                    "values_range": [0, 10000],
                    "compression_type": "LZW",
                },
                "product_list": ["IS51010", "IS51011"],
                "s3_bucket_names": ["satsure-satimg", "satimg-to-be-deleted"],
            },
            "cs": {
                "entry": {},
                "exit": {
                    "filename_parts_count": 4,
                    "filename_endswith": ".tif",
                    "filename_date_chars": 8,
                    "filename_product_code": ["CS"],
                    "filename_product_code_count": 7,
                    "filename_season_code_count": 4,
                    "filename_season_code_startswith": ["K", "R"],
                    "epsg_code_count": 5,
                    "pixelsize": "10.0 -10.0",
                    "nodata_value": "0.0",
                    "values_range": [0, 1],
                    "compression_type": "LZW",
                },
                "product_list": ["CS"],
                "s3_bucket_names": ["satsure-products"],
            },
            "ch": {
                "entry": {},
                "exit": {
                    "filename_parts_count": 4,
                    "filename_endswith": ".tif",
                    "filename_date_chars": 8,
                    "filename_product_code": ["CH"],
                    "filename_product_code_count": 7,
                    "filename_season_code_count": 4,
                    "filename_season_code_startswith": ["K", "R"],
                    "epsg_code_count": 5,
                    "pixelsize": "10.0 -10.0",
                    "nodata_value": "0.0",
                    "values_range": [0, 1],
                    "compression_type": "LZW",
                },
                "product_list": ["CH"],
                "s3_bucket_names": ["satsure-products"],
            },
        }
        self.product = self._fetch_product()

    def _fetch_product(self):
        """
        Fetch product name from file path

        Returns:
            str: name of the product for the input file
        """
        file_parts = self.file.split("/")
        for product_name, details in self.checks_json.items():
            if file_parts[-2] in details.get("product_list", []) and file_parts[
                2
            ] in details.get("s3_bucket_names", []):
                return product_name

    def _entry_values_computer(self, metadata: MetadataModel) -> QaQcModel:
        """
        Compute additional entry values based on extracted metadata.

        Args:
            metadata (MetadataModel): Extracted metadata.

        Returns:
            QaQcModel
        """
        meta_fileparts = metadata.filename.split("_")
        computed_check_values = QaQcModel()
        computed_check_values.filename_parts_count = len(meta_fileparts)
        computed_check_values.filename_endswith = metadata.filename[-4:]
        computed_check_values.filename_date_chars = len(meta_fileparts[0])
        computed_check_values.filename_product_code = meta_fileparts[2].split(".")[0]
        computed_check_values.filename_product_code_count = len(
            meta_fileparts[2].split(".")[0]
        )
        computed_check_values.filename_season_code_count = (
            len(meta_fileparts[3].split(".")[0]) if len(meta_fileparts) > 3 else 0
        )
        computed_check_values.filename_season_code_startswith = (
            meta_fileparts[3][:1] if len(meta_fileparts) > 3 else ""
        )
        # computed_check_values.epsg_code_count = ""
        computed_check_values.pixelsize = metadata.pixelsize
        computed_check_values.nodata_value = metadata.nodata
        computed_check_values.values_range = [int(metadata.min), int(metadata.max)]
        computed_check_values.compression_type = metadata.compression

        return computed_check_values

    def main(self) -> None:
        """
        Main function to orchestrate metadata extraction,
        QA/QC checks, and pushing to DynamoDB.
        """
        metadata_obj = MetaData(self.file)
        metadata = metadata_obj.main()
        if metadata:
            logging.info("started computing metadata")
            computed_values = self._entry_values_computer(metadata)
            logging.info("started qaqc")
            qa_qc = QaQc(self.checks_json)
            checks = qa_qc.main(computed_values, self.product, self.check_type)
            logging.info("qaqc done")
            metadata.metadata_check = checks["metadata_check"]
            print(metadata)
            return {
                "statusCode": 200,
                "body": {
                    "message": "metadata extraction successful",
                    "metadata": asdict(metadata),
                },
            }
        else:
            return {"statusCode": 500, "body": "metadata extraction not successful"}
