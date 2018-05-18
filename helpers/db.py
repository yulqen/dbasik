from datamap.models import Datamap


def delete_datamap(dm: Datamap) -> None:
    """Delete all DatamapLine objects belonging to a datamap."""
    dmls = dm.datamapline_set.all()
    dmls.delete()
