from helpers.file_processors import _validate_dmlines_from_csv


def test_csv_processor(uploaded_csv_file_bytes):

    assert _validate_dmlines_from_csv(uploaded_csv_file_bytes) == (4, [])
