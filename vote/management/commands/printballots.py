from django.core.management.base import BaseCommand, CommandError

from vote.models import Category, BallotCategory

class Command(BaseCommand):
    args = ''
    help = 'Prints the ballots in a human-readable format'

    def handle(self, *args, **options):
        for category in Category.objects.all():
          print u'=== {category.title}'.format(**locals())

          for ballot_category in category.ballotcategory_set.all():
            for ballot_option in ballot_category.ballotoption_set.all():
              print ballot_option.option_id,

            print