from django.core.management.base import BaseCommand, CommandError
from core.models import Process, Part
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
from core.models import Process, Part


def fix_text(x): return ''.join(x).strip()


class Command(BaseCommand):
    help = 'Get the process'

    def handle(self, *args, **options):
        process_list = ['processo-01.html', 'processo-02.html']

        for process in process_list:

            try:
                url = f"https://thick-theory.surge.sh/{process}"

                self.stdout.write(self.style.WARNING(url))

                response = requests.get(url)

                response.raise_for_status()

                html_page = response.text

                tree = html.fromstring(html_page)

                number = fix_text(tree.xpath(
                    '/html/body/div/div[1]/div/h4[1]/text()'))
                judge = fix_text(tree.xpath(
                    '/html/body/div/div[3]/div[1]/span/text()'))

                process_class = fix_text(tree.xpath(
                    '/html/body/div/div[2]/div[1]/span/text()'))

                subject = fix_text(tree.xpath(
                    '/html/body/div/div[2]/div[3]/span/text()'))

                self.stdout.write(self.style.SUCCESS(
                    'Process number "%s"' % number))
                self.stdout.write(self.style.SUCCESS(
                    'Process judge "%s"' % judge))
                self.stdout.write(self.style.SUCCESS(
                    'Process class "%s"' % process_class))
                self.stdout.write(self.style.SUCCESS(
                    'Process subject "%s"' % subject))

                process = Process(
                    number=number,
                    judge=judge,
                    process_class=process_class,
                    subject=subject
                )

                process.save()

                parts = tree.xpath('/html/body/div/div[4]/div/ul/li')

                for p in parts:
                    name = p.xpath('span[1]/text()')[0].strip()
                    category = ''.join(
                        p.xpath('span[contains(@class,"badge-warning")]/text()')).strip()

                    part = Part(
                        process=process,
                        name=name,
                        category=category
                    )
                    part.save()

            except HTTPError as http_err:
                raise CommandError(f'HTTP error occurred: {http_err}')
            except Exception as err:
                raise CommandError(f'Other error occurred: {err}')

            self.stdout.write(self.style.SUCCESS(
                'Successfully process "%s"' % process))
