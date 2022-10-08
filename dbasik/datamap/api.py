from typing import List

from ninja import ModelSchema, Router

from .models import Datamap, DatamapLine

router = Router()


class DatamapLineSchema(ModelSchema):
    class Config:
        model = DatamapLine
        model_fields = ["id", "datamap", "key", "data_type", "sheet", "cell_ref"]


class DatamapSchema(ModelSchema):
    class Config:
        model = Datamap
        model_fields = ["id", "name", "tier", "active", "slug"]


@router.get("/datamap", response=List[DatamapLineSchema])
def datamap_detail_api(request, slug: str):
    return DatamapLine.objects.filter(datamap__slug=slug).order_by("id")


@router.get("/datamaps", response=List[DatamapSchema])
def datamaps(request):
    return Datamap.objects.all()
