import os
import tempfile


def csv_incorrect_headers():
    tmpdir = tempfile.gettempdir()
    uf = os.path.join(tmpdir, "bad_datamap.csv")
    with open(uf, "w") as f:
        f.write("bad_key,bad_sheet,bad_cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf


def csv_correct_headers():
    tmpdir = tempfile.gettempdir()
    uf = os.path.join(tmpdir, "good_datamap.csv")
    with open(uf, "w") as f:
        f.write("key,sheet,cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf