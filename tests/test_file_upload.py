import pytest

from datamap import models


@pytest.mark.django_db
def test_get_model_instances():
    dm_lines = models.DatamapLine.objects.all()
    assert dm_lines[0].key == 'SRO First Name'
