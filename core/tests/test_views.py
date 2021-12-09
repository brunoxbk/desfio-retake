from django.test import TestCase
from core.models import Process, Part
from django.urls import reverse_lazy


class ViewsTestCase(TestCase):

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

    def test_index_load(self):
        response = self.client.get(reverse_lazy('core:list'))
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        process = Process.objects.last()
        response = self.client.get(reverse_lazy(
            'core:detail', kwargs={'pk': process.pk}))
        self.assertEqual(response.status_code, 200)
