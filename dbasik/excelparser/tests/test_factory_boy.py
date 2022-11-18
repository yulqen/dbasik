from django.test import TestCase

from dbasik.factories.datamap_factories import DatamapFactory, DatamapLineFactory


class EnsureFactoryBoyObjects(TestCase):
    def setUp(self):
        self.dmf = DatamapFactory()
        self.dml = DatamapLineFactory()
        self.dml_params = DatamapLineFactory(
            key="Test Own Key", sheet="Test Own Sheet", cell_ref="A10"
        )

    def test_can_create_datamap_factory(self):
        self.assertTrue(self.dmf.name, "Test Datamap from Factory")

    def test_datamapline_for_datamap_factory(self):
        self.assertTrue(self.dml.key, "Test Key")
        self.assertTrue(self.dml.sheet, "Test Sheet")
        self.assertTrue(self.dml.cell_ref, "Test Cell_Ref")

    def test_datamapline_for_datamap_factory_own_params(self):
        self.assertTrue(self.dml_params.key, "Test Own Key")
        self.assertTrue(self.dml_params.sheet, "Test Own Sheet")
        self.assertTrue(self.dml_params.cell_ref, "Test Own Cell_Ref")
