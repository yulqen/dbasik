from typing import List

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router

from .models import Tier

router = Router()


class TierSchema(ModelSchema):
    class Config:
        model = Tier
        model_fields = ["id", "name", "description", "slug"]


@router.get("/tiers/{tier_id}", response=TierSchema)
def tiers(request, tier_id: int):
    return get_object_or_404(Tier, id=tier_id)


@router.get("/tiers", response=List[TierSchema])
def tiers(request):
    return Tier.objects.all()
