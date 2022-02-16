import os
import tempfile

TEMPDIR = tempfile.gettempdir()


def csv_repeating_lines() -> str:
    """
    Generate path to csv for use in tests. Contains headers
    which repeat and will not be allowed into a Datamap table
    due to unique constraints.
    """
    uf: str = os.path.join(TEMPDIR, "csv_repeating_lines.csv")
    with open(uf, "w") as f:
        f.write("key,sheet,cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("First row col 1,First row col 2,A15\n")
    return uf


def csv_incorrect_headers() -> str:
    """
    Generate path to csv for use in tests. Contains headers which
    are not allowed by the system.
    """
    uf: str = os.path.join(TEMPDIR, "bad_datamap.csv")
    with open(uf, "w") as f:
        f.write("bad_key,bad_sheet,bad_cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf


def csv_correct_headers() -> str:
    """
    Generate path to csv for use in tests. Contains headers appropriate
    for the system.
    """
    uf: str = os.path.join(TEMPDIR, "good_datamap.csv")
    with open(uf, "w") as f:
        f.write("key,sheet,cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf


def csv_containing_hundred_plus_length_key() -> str:
    """
    Generate path to csv for use in tests. Contains a single
    header which is too long to be used by the system.
    """
    uf: str = os.path.join(TEMPDIR, "big_key_csv.csv")
    k = (
        "This is a key that is way too long and need to be "
        "seriously truncated we dont like keys this length do we?"
    )
    with open(uf, "w") as f:
        f.write("key,sheet,cell_ref\n")
        f.write(f"{k},First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf
