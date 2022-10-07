from django.core.validators import FileExtensionValidator, RegexValidator

acceptable_types = ["csv"]
file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a valid CSV file type."
)
cell_ref_validator = RegexValidator(
    regex=r"^([A-Z]|[a-z]){1,3}\d+$",
    message="The cell_ref field must in Excel cell reference format, e.g. 'A10'.",
)
