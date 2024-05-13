from typing import Dict

from qa_qc_check.model.metadata_model import QaQcModel
from qa_qc_check.validator.meta_data_validator import (
    FilenameProductCodeValidator,
    FileNameSeasonCodeValidator,
    ValuesRangeValidator,
)


class QaQc:

    VALIDATORS = {
        "filename_product_code": FilenameProductCodeValidator,
        "filename_season_code_startswith": FileNameSeasonCodeValidator,
        "values_range": ValuesRangeValidator,
    }

    def __init__(self, checks_json):
        self.checks = checks_json

    def main(
        self, entry_values_metadata: QaQcModel, product: str, check_type: str
    ) -> Dict:
        """
        Perform QA/QC checks on computed entry values.

        Args:
            entry_values_metadata (QaQcModel): Computed entry values.

        Returns:
            dict: Results of QA/QC checks.
        """
        product_checks = self.checks.get(product, {}).get(check_type, {})
        results = {}
        for check_name, actual_value in vars(entry_values_metadata).items():
            expected_value = product_checks[check_name]
            if check_name in self.VALIDATORS:
                validator = self.VALIDATORS[check_name]
                results[check_name] = validator(product).validate(
                    actual_value, expected_value
                )
            else:
                results[check_name] = actual_value == expected_value
        metadata_result = "Passed" if all(results.values()) else "Failed"

        return {"metadata_check": metadata_result}
