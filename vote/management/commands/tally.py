# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError

from pyvotecore.schulze_method import SchulzeMethod

from vote.models import Category, Option, BallotCategory

class Command(BaseCommand):
    args = ''
    help = 'Tallies the votes and prints the winners'

    def handle(self, *args, **options):
        for category in Category.objects.all():
          print u'=== {category.title}'.format(**locals())
          print

          category_input = []

          for ballot_category in category.ballotcategory_set.all():
            ballot_options = ballot_category.ballotoption_set.all().order_by('order')
            category_input.append(dict(
              count=1,
              ballot=[[ballot_option.option_id] for ballot_option in ballot_options]
            ))

          if category_input:
            category_result = SchulzeMethod(category_input, ballot_notation='grouping').as_dict()

            if 'tied_winners' in category_result:
              print 'JAETTU VOITTO:'

              for tied_winrar in category_result['tied_winners']:
                print Option.objects.get(id=tied_winrar).title

            elif 'winner' in category_result:
              print Option.objects.get(id=category_result['winner']).title

          else:
            print u'EI ÄÄNIÄ'

          print