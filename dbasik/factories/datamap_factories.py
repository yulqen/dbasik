import factory

from dbasik.datamap.models import Datamap
from dbasik.datamap.models import DatamapLine
from dbasik.register.models import Project
from dbasik.register.models import ProjectStage
from dbasik.register.models import ProjectType
from dbasik.register.models import Tier
from dbasik.users.models import DfTGroup


class TierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tier

    name = "Test Tier from Factory"
    slug = "test-tier-from-factory"
    description = "Description for Tier object"


class DatamapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Datamap
        django_get_or_create = ("name", "tier")

    name = "Test Datamap from Factory"
    tier = factory.SubFactory(TierFactory)


class DatamapLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DatamapLine

    datamap = factory.SubFactory(DatamapFactory)
    key = "Test key"
    sheet = "Test sheet"
    cell_ref = "A1"


class ProjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectType

    name = factory.Faker("name")


class DfTGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DfTGroup

    name = "Test DfTGroup from Factory"


class ProjectStageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectStage

    name = "Test Stage"


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = "Test Project"
    tier = factory.SubFactory(TierFactory)
    project_type = factory.SubFactory(ProjectTypeFactory)
    stage = factory.SubFactory(ProjectStageFactory)
    dft_group = factory.SubFactory(DfTGroupFactory)
