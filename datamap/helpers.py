from django.db import IntegrityError

from datamap.models import DatamapLine, Datamap


def _save_or_except(dm: Datamap, **kwargs) -> DatamapLine:
    """
    Attempts to save a Datamapline object to a Datamap object.
    kwargs must contain correct keys for adding a Datamapline.
    The function throws an IntegrityError with a helpful message
    if a DatamapLine already exists for that Datamap with those
    parameters.

    If the database save is success, the DatamapLine object is returned.
    :param dm:
    :type dm: datamap.models.Datamap
    :param kwargs:
    :type dict:
    :return: DatamapLine
    :rtype: DatamapLine
    """
    try:
        dml = DatamapLine.objects.create(datamap=dm, **kwargs)
        return dml
    except IntegrityError:
        err_str = _parse_kwargs_to_error_string(kwargs)
        raise IntegrityError(f"{err_str} already appears in Datamap: {dm.name}")


def _parse_kwargs_to_error_string(datamap: Datamap, kwargs: dict) -> str:
    err_lst = []
    err_stmt = []
    for x in kwargs.items():
        err_lst.append(x)
    for x in err_lst:
        err_stmt.append(f"{x[0]}: {x[1]}")
    return f"Database Error: {' '.join([x for x in err_stmt])} already appears in Datamap: {datamap}"
