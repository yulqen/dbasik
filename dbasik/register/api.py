from typing import List

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router

from .models import FinancialQuarter, Project, Tier

router = Router()


class TierSchema(ModelSchema):
    class Config:
        model = Tier
        model_fields = ["id", "name", "description", "slug"]


class ProjectSchema(ModelSchema):
    class Config:
        model = Project
        model_fields = "__all__"


class FQSchema(ModelSchema):
    class Config:
        model = FinancialQuarter
        model_fields = "__all__"


@router.get("/tiers/{tier_id}", response=TierSchema)
def tier(request, tier_id: int):
    return get_object_or_404(Tier, id=tier_id)


@router.get("/tiers", response=List[TierSchema])
def tiers(request):
    return Tier.objects.all()


@router.get("/projects", response=List[ProjectSchema])
def projects(request):
    return Project.objects.all()


@router.get("/projects/{project_id}", response=ProjectSchema)
def project(request, project_id):
    return get_object_or_404(Project, id=project_id)


@router.get("/financialquarters", response=List[FQSchema])
def financialquarters(request):
    return FinancialQuarter.objects.all()


@router.get("/financialquarters/{fq_id}", response=FQSchema)
def financialquarter(request, fq_id):
    return get_object_or_404(FinancialQuarter, id=fq_id)
