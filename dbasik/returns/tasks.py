from celery import shared_task

from celery import shared_task

from dbasik.datamap.models import Datamap
from dbasik.excelparser.helpers.parser import ParsedSpreadsheet
from dbasik.register.models import FinancialQuarter, Project
from dbasik.returns.models import Return


@shared_task
def process_batch(fq_id, dm_id, save_path, project_name):
    fq = FinancialQuarter.objects.get(pk=fq_id)
    datamap = Datamap.objects.get(pk=dm_id)
    project = Project.objects.get(name=project_name)
    # make idempotent
    # does this Return exist already?
    if Return.objects.filter(financial_quarter=fq, project=project).exists():
        r = Return.objects.get(financial_quarter=fq, project=project)
        r.delete()
        return_obj = Return.objects.create(
            project=project,
            financial_quarter=fq
        )
    else:
        return_obj = Return.objects.create(
            project=project,
            financial_quarter=fq
        )
    try:
        parsed_spreadsheet = ParsedSpreadsheet(save_path, project, return_obj, datamap)
    except ImportError:
        raise
    parsed_spreadsheet.process()
    print(f"{save_path} processed successfully")
