from django.core.management.base import BaseCommand
from wedding.models import *
import csv

CODE = 'CODE'
GROUP_NAME = 'Group Name'
EMAIL = 'Email'
ADDRESS_1 = 'Address 1'
ADDRESS_2 = 'Address 2'
ADDRESS_3 = 'Address 3'

# Filter out of master CSV based on who we want to import
def include_criteria(row):
    return row['Person 1'] and row['Needs STD']

def get_names(row):
    return [
        row[col] for col in ['Person 1', 'Person 2',
                      'Kid 1', 'Kid 2', 'Kid 3',
                      'Kid 4', 'Kid 5']
        if row[col]
    ]

class Command(BaseCommand):
    help = 'Import groups and people from the master list CSV'

    def add_arguments(self, parser):
        parser.add_argument('input_path')

    def _import_csv(self, input_path):
        rehearsal = Event.objects.get(short_name='rehearsal')
        festival = Event.objects.get(short_name='festival')
        ceremony = Event.objects.get(short_name='ceremony')

        with open(input_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in filter(include_criteria, reader):
                code = row[CODE]
                print(code)
                existing = Group.objects.filter(pnr=code)
                if existing:
                    if len(existing) > 1:
                        raise Exception('Houstin we have a problem. '
                                        'Duplicate groups for code %s'.format(code))
                    group = existing[0]
                    print('exists')
                else:
                    group = Group(pnr=code)

                group.display_name = row[GROUP_NAME]
                group.main_email = row[EMAIL]
                group.address_1 = row[ADDRESS_1]
                group.address_2 = row[ADDRESS_2]
                group.address_3 = row[ADDRESS_3]

                group.save()

                # Events
                if row['Rehearsal'] == 'x':
                    group.events.add(rehearsal)
                else:
                    group.events.remove(rehearsal)

                for event in [ceremony, festival]:
                    group.events.add(event)

                group.save()

                # People
                names = get_names(row)
                print(names)
                for name in names:
                    existing = Person.objects.filter(name=name)
                    if existing:
                        if len(existing) > 1 and name != 'Guest':
                            raise Exception('Houstin we have a problem. '
                                            'Duplicate person for name %s'.format(name))
                        elif name == 'Guest':
                            person = Person(name=name)
                        else:
                            person = existing[0]
                    else:
                        person = Person(name=name)

                    person.group = group
                    person.name_flagged = False

                    person.save()

                print(code)

        print("YES")

    def handle(self, *args, **options):
        self._import_csv(options['input_path'])
