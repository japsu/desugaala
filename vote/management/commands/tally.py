# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError

from vote.models import Category, Option, BallotCategory

class Command(BaseCommand):
    args = ''
    help = 'Tallies the votes and prints the winners'

    def handle(self, *args, **options):
        for category in Category.objects.all():
          print u'=== {category.title}'.format(**locals())
          print

          category_result = category.evaluate()

          if category_result:
              if 'tied_winners' in category_result:
                  print 'JAETTU VOITTO:'

                  for tied_winrar in category_result['tied_winners']:
                      print tied_winrar.title

              elif 'winner' in category_result:
                  print category_result['winner'].title

          else:
              print u'EI ÄÄNIÄ'

          print