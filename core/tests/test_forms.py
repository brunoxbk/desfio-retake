from django.forms import formsets
from django.test import TestCase
from core.forms import ProcessForm, PartFormSet


class ViewsTestCase(TestCase):

    def test_process_valid_form(self):
        data = {
            "number": "1009999-99.2021.0.00.0123",
            "judge": "Uncle Phill",
            "process_class": "Busca e Apreensão",
            "subject": "Alienação Fiduciária"
        }
        form = ProcessForm(data=data)
        self.assertTrue(form.is_valid())

    def test_process_invalid_form(self):
        data = {
            "number": "",
            "judge": "Uncle Phill",
            "process_class": "Busca e Apreensão",
            "subject": ""
        }
        form = ProcessForm(data=data)
        self.assertFalse(form.is_valid())

    def test_part_valid_form(self):
        data = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            "form-0-name": "Du",
            "form-0-category": "REQUERIDO",
            "form-1-name": "DuDu",
            "form-1-category": "REQUERIDO",
            "form-2-name": "Edu",
            "form-2-category": "REQUERENTE",
        }
        formset = PartFormSet(data=data)
        self.assertTrue(formset.is_valid())

    def test_process_invalid_form(self):
        data = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            "form-0-name": "Du",
            "form-0-category": "",
            "form-1-name": "DuDu",
            "form-1-category": "",
            "form-2-name": "",
            "form-2-category": "REQUERENTE",
        }
        formset = PartFormSet(data=data)
        self.assertFalse(formset.is_valid())
