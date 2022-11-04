from django.core.management.base import BaseCommand, CommandError

from dbasik.register.models import Tier, ProjectType, ProjectStage, DfTGroup
from dbasik.register.models import Project


class Command(BaseCommand):
    help = """
    Sets up project entities in database.
    """

    def handle(self, *args, **options):
        tier_list = ["Tier 1", "Tier 2", "Tier 3"]
        for x in tier_list:
            Tier.objects.create(name=x)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created Tier {x}"
                )
            )

        type_list = ["project", "programme"]
        for x in type_list:
            ProjectType.objects.create(name=x)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created type {x}"
                )
            )

        stage_list = ["pre-SOBC", "SOBC", "OBC", "FBC"]
        for x in stage_list:
            ProjectStage.objects.create(name=x)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created stage {x}"
                )
            )

        group_list = ["CDG", "HSRG", "RPE", "RIG"]
        for x in group_list:
            DfTGroup.objects.create(name=x)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created DfT group {x}"
                )
            )

        projects_dictionary = {
            "Government Boots": "GB",
            "Liquid Soul": "LS",
            "Methodist Protest": "MP",
            "Move and Improve": "M&I",
            "Pied Piper": "PP",
            "Quakers and Shakers": "Q&S",
            "Rat around the corner": "RATC",
            "The Left Right": "TLR",
            "Two Step Shuffle": "TSS",
        }

        for x in projects_dictionary:
            tier = Tier.objects.order_by("?").first()
            group = DfTGroup.objects.order_by("?").first()
            p_type = ProjectType.objects.order_by("?").first()
            stage = ProjectStage.objects.order_by("?").first()
            Project.objects.create(
                name=x,
                tier=tier,
                project_type=p_type,
                stage=stage,
                abbreviation=projects_dictionary[x],
                dft_group=group,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created Project {x}"
                )
            )
