import factory
import pytest

from templates import models


class TemplateFactory(factory.Factory):
    class Meta:
        model = models.Template

    name = "Test Factory Template"
    description = "Test Factory Description"
    source_file = "path/to/template.xlsx"
    slug = "test-factory-template"


def test_basic_model():
    template_obj = TemplateFactory.create()
    assert template_obj.name == "Test Factory Template"
