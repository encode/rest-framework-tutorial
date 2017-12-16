from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Restores database to fresh state.'

    def handle(self, *args, **options):
        call_command('flush', '--noinput')
        call_command('loaddata', 'snippets/fixtures/users.json')
        self.stdout.write(self.style.SUCCESS('Successfully restored database'))
