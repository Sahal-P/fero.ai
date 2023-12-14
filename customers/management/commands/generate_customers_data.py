# your_app/management/commands/generate_mock_data.py
import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from customers.models import Customer
from django.db.models import Q


class Command(BaseCommand):
    help = 'Generate mock data for your app'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        random.seed(42)  # Set a seed for reproducibility

        # Add your Customer model and the number of instances you want to create
        seeder.add_entity(Customer, 10, {
            'name': lambda x: seeder.faker.name(),
            'contact_number': lambda x: seeder.faker.random_int(min=1000000000, max=9999999999),
            'email': lambda x: seeder.faker.email(),
        })

        inserted_pks = seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'Successfully inserted data with primary keys: {inserted_pks}'))
