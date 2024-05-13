from abc import ABC, abstractmethod


class ValidatorInterface(ABC):
    def __init__(self, product):
        self.product = product

    @abstractmethod
    def validate(self, actual_value: any, expected_value: any):
        pass


class FilenameProductCodeValidator(ValidatorInterface):
    """Validator class for Product code validation"""

    def validate(self, actual_value: str, expected_value: list):
        """Method to validate the product code

        Args:
            actual_value (str): Actual product code value
            expected_value (list): Expected porduct code values

        Returns:
            bool
        """
        if self.product in ["cs", "ch"]:
            results = expected_value[0] in actual_value
            return results
        else:
            results = actual_value in expected_value
            return results


class FileNameSeasonCodeValidator(ValidatorInterface):
    """Validator class for Season code validation"""
    def validate(self, actual_value: str, expected_value: list):
        """Method to validate season code

        Args:
            actual_value (str): Actual season code value
            expected_value (list): Expected season code values

        Returns:
            bool
        """
        results = actual_value in expected_value
        return results


class ValuesRangeValidator(ValidatorInterface):
    """Validator class for value range validation"""
    def validate(self, actual_value: list, expected_value: list):
        """Method to validate the Min and Max value range

        Args:
            actual_value (list): Actual Min, Max value range
            expected_value (list): Expected Min, Max value range

        Returns:
            bool
        """
        results = (
            actual_value[0] >= expected_value[0] or actual_value[1] <= expected_value[1]
        )
        return results
