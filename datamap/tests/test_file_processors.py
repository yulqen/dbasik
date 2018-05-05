from helpers.file_processors import add_datamaplines_from_csv


def test_csv_processor(uploaded_csv_file_bytes):

    assert add_datamaplines_from_csv(uploaded_csv_file_bytes) == (3, [])
