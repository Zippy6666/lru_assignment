from django.core.management.base import BaseCommand
from lru_web_app.models import Person
from faker import Faker
from threading import Thread # TODO


SEED_DATA_COUNT: int = 1_000_000
BATCH_SIZE: int = SEED_DATA_COUNT//100


def to_person_number(num: int) -> str:
    num = str(num)
    personnummer = f"{num[0:8]}-{num[8:12]}"
    return personnummer


class Command(BaseCommand):
    help = "Seeds data into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE(f"Trying to seed data... {args} {kwargs}"))

        Person.objects.all().delete()
        self.stdout.write(self.style.NOTICE('Removed any old "Person" instances...'))

        fake = Faker()
        objects = []
        self.stdout.write(self.style.NOTICE("Instanciating objects, please wait..."))
        bulk_creations = 0
        for _ in range(SEED_DATA_COUNT):
            city = fake.city()
            person_number = to_person_number(
                fake.random_number(digits=12, fix_len=True)
            )
            name = fake.name()
            job = fake.job()
            country = fake.country()
            phone_number = fake.phone_number()
            person = Person(
                name=name,
                job=job,
                country=country,
                phone_number=phone_number,
                person_number=person_number,
                city=city,
            )
            objects.append(person)

            if len(objects) >= BATCH_SIZE:
                objects.clear()
                Person.objects.bulk_create(objects)
                bulk_creations += 1
                self.stdout.write(self.style.SUCCESS(f"{bulk_creations}/{SEED_DATA_COUNT//BATCH_SIZE} batches done!"))


        first_person = Person.objects.first()
        name = first_person.name
        person_number = first_person.person_number
        phone_number = first_person.phone_number
        self.stdout.write(
            self.style.SUCCESS(
                f"Sucess! Example person: {name} {person_number} {phone_number}"
            )
        )
