import string
import os

from celery import shared_task
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.core.files.storage import default_storage

from register.models import FinancialQuarter, ProjectStage, Project
from returns.models import Return
from excelparser.helpers.parser import ParsedSpreadsheet
from datamap.models import Datamap


@shared_task
def process_batch(fq_id, dm_id, save_path, project_name) -> HttpResponseRedirect:
    print(project_name)
    print(save_path)
    fq = FinancialQuarter.objects.get(pk=fq_id)
    datamap = Datamap.objects.get(pk=dm_id)
    project = Project.objects.get(name=project_name)
    return_obj = Return.objects.create(
        project=project,
        financial_quarter=fq
    )
    parsed_spreadsheet = ParsedSpreadsheet(save_path, project, return_obj, datamap)
    parsed_spreadsheet.process()
    print(f"{save_path} processed successfully")
