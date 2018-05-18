# to do

import pytest

from datamap.models import Datamap
from helpers import delete_datamap


@pytest.mark.django_db
def test_delete_datamap(datamaplines_for_single_datamap, django_db_setup):
    dm = Datamap.objects.get(pk=datamaplines_for_single_datamap)
    assert dm.name == "Datamap 1"
    dmls = dm.datamapline_set.all()
    delete_datamap(dm)
    assert len(dmls) == 0
