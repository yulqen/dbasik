from typing import List

from dbasik.register.api import TierSchema
from ninja import ModelSchema, Router, Schema

from .models import Datamap, DatamapLine

router = Router()


# class DatamapSchema(ModelSchema):
#     class Config:
#         model = Datamap
#         model_fields = ["id", "name", "tier", "active", "slug"]


class DatamapSchema(Schema):
    id: int
    name: str
    tier: TierSchema
    active: bool
    slug: str


class DatamapLineSchema(Schema):
    id: int
    datamap: DatamapSchema
    key: str
    data_type: str
    sheet: str
    cell_ref: str


# class DatamapLineSchema(ModelSchema):
#     class Config:
#         model = DatamapLine
#         model_fields = ["id", "datamap", "key", "data_type", "sheet", "cell_ref"]


@router.get("/datamap", response=List[DatamapLineSchema])
def datamap(request, slug: str):
    return DatamapLine.objects.filter(datamap__slug=slug).order_by("id")


@router.get("/datamaps", response=List[DatamapSchema])
def datamaps(request):
    return Datamap.objects.all()
