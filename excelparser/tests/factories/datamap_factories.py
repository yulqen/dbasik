import factory
from datamap.models import Datamap, DatamapLine
from register.models import Tier


class TierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tier

    name = "Test Tier from Factory"
    slug = "test-tier-from-factory"
    description = "Description for Tier object"


class DatamapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Datamap
        django_get_or_create = ('name', 'tier')

    name = "Test Datamap from Factory"
    tier = factory.SubFactory(TierFactory)


class DatamapLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DatamapLine

    datamap = factory.SubFactory(DatamapFactory)
    key = "Test key"
    sheet = "Test sheet"
    cell_ref = "Test Cell_Ref"


class ProjectFactory(object):
    pass