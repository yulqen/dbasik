import os
import factory
import pytest

from templates import models


class TemplateFactory(factory.Factory):
    class Meta:
        model = models.Template

    name = "Test Factory Template"
    description = "Test Factory Description"
    source_file = "macro_enabled_template.xlsm"
    slug = "test-factory-template"


def test_basic_model():
    template_obj = TemplateFactory.create()
    assert template_obj.name == "Test Factory Template"
    assert template_obj.source_file == "macro_enabled_template.xlsm"

