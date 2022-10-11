from typing import List

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router, Schema

from .models import FinancialQuarter, Project, ProjectStage, ProjectType, Tier

router = Router()


class TierSchema(ModelSchema):
    class Config:
        model = Tier
        model_fields = ["id", "name", "description", "slug"]


class ProjectTypeSchema(ModelSchema):
    class Config:
        model = ProjectType
        model_fields = "__all__"


class ProjectStageSchema(ModelSchema):
    class Config:
        model = ProjectStage
        model_fields = "__all__"


class ProjectSchema(Schema):
    id: int
    slug: str
    name: str
    project_type: ProjectTypeSchema = None
    stage: ProjectStageSchema = None
    abbreviation: str
    tier: TierSchema = None  # optional, as per docs


# class ProjectSchema(ModelSchema):
#     class Config:
#         model = Project
#         model_fields = "__all__"


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
    queryset = Project.objects.select_related("tier")
    return list(queryset)


@router.get("/projects/{project_id}", response=ProjectSchema)
def project(request, project_id):
    project = Project.objects.select_related("tier").get(id=project_id)
    return project


@router.get("/financialquarters", response=List[FQSchema])
def financialquarters(request):
    return FinancialQuarter.objects.all()


@router.get("/financialquarters/{fq_id}", response=FQSchema)
def financialquarter(request, fq_id):
    return get_object_or_404(FinancialQuarter, id=fq_id)
