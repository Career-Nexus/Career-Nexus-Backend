from django.core.management.base import BaseCommand

from info.models import *

import sys
import json
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open("NOTES/permitted_countries.json","r") as file:
            countries = json.load(file)
        sys.stdout.write(self.style.SUCCESS("Loading default countries into the system. PLEASE WAIT.....\n\n"))
        time.sleep(4)
        count = 0
        for country in countries:
            count +=1
            name = country["country"]
            code = country["code"]
            permitted = True
            Countrycodes.objects.get_or_create(country=name,code=code,permitted=permitted)

        sys.stdout.write(self.style.SUCCESS(f"Loaded {count} countries and codes into the system."))

