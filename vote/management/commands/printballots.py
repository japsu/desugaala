from django.core.management.base import BaseCommand, CommandError

from vote.models import Category, BallotCategory

class Command(BaseCommand):
    args = ''
    help = 'Prints the ballots in a human-readable format'

    def handle(self, *args, **options):
        for category in Category.objects.all():
          print u'=== {category.title}'.format(**locals())
          print

          for ballot_category in category.ballotcategory_set.all():
            for index, ballot_option in enumerate(ballot_category.ballotoption_set.all().order_by('order')):
              index += 1
              option = ballot_option.option
              print u'{index}. {option.title}'.format(**locals())

            print