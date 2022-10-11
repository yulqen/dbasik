from typing import List

from dbasik.datamap.api import DatamapLineSchema
from dbasik.register.api import FQSchema, ProjectSchema
from dbasik.returns.models import Return
from django.shortcuts import get_object_or_404
from ninja import Router, Schema

router = Router()


class ReturnSchema(Schema):
    id: int
    project: ProjectSchema = None
    financial_quarter: FQSchema = None


class ReturnItemSchema(Schema):
    id: int
    parent: ReturnSchema = None
    datamapline: DatamapLineSchema = None
    value_str: str = None
    value_int: int = None
    value_float: float = None
    value_date: str = None
    value_datetime: str = None
    value_phone: str = None


@router.get("/returns", response=List[ReturnSchema])
def returns(request):
    return Return.objects.all()


@router.get("/returns/{return_id}", response=ReturnSchema)
def return_(request, return_id):
    return get_object_or_404(Return, id=return_id)
