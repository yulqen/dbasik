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
