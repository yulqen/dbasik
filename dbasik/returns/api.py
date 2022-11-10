import datetime
from typing import List

from dbasik.datamap.api import DatamapLineSchema
from dbasik.register.api import FQSchema, ProjectSchema
from dbasik.returns.models import Return, ReturnItem
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
    value_date: datetime.date = None
    value_datetime: datetime.datetime = None
    value_phone: str = None


@router.get("/returns", response=List[ReturnItemSchema])
def returns(request):
    """Top level Return items, without the data."""
    return Return.objects.all()


@router.get("/returns/{return_id}", response=ReturnSchema)
def return_(request, return_id):
    return get_object_or_404(Return, id=return_id)


@router.get("/returns-for-quarter/{quarter_id}",
            response=List[ReturnItemSchema])
def returns_for_quarter(request, quarter_id: int):
    return ReturnItem.objects.filter(parent__financial_quarter=quarter_id)
