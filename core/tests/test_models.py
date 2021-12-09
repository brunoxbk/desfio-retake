from django.test import TestCase

from core.models import Process, Part


class ProcessTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        process = Process.objects.create(
            number="1009999-99.2021.0.00.0999",
            judge="Sérgio Moro",
            process_class="Busca e Apreensão",
            subject="Alienação Fiduciária"
        )

        Part.objects.create(
            process=process,
            name="Patrik",
            category="REQUERIDO"
        )

        Part.objects.create(
            process=process,
            name="Bob Esponja",
            category="REQUERENTE"
        )

    def test_creation(self):
        process = Process.objects.first()
        self.assertTrue(isinstance(process, Process))

    def test_parts(self):
        process = Process.objects.first()
        parts = process.parts.all()
        self.assertGreater(len(parts), 1)
