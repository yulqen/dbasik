from typing import List

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router

from .models import Project, Tier

router = Router()


class TierSchema(ModelSchema):
    class Config:
        model = Tier
        model_fields = ["id", "name", "description", "slug"]


class ProjectSchema(ModelSchema):
    class Config:
        model = Project
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
