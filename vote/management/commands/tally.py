# encoding: utf-8

from pprint import pprint
from itertools import islice

from django.core.management.base import BaseCommand, CommandError

from vote.models import Category, Option, BallotCategory
from status.models import Watch

# http://stackoverflow.com/a/6822773/1012299
def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

class Command(BaseCommand):
    args = ''
    help = 'Tallies the votes and prints the winners'

    def handle(self, *args, **options):
        for category in Category.objects.all():
          print u'=== {category.title}'.format(**locals())
          print

          category_result = category.evaluate()

          if category_result:
            for index, (current, runner_up) in enumerate(window(category_result['order'])):
                index += 1

                # XXX hack
                watch = Watch.objects.create(category=category)
                watch.watchoption_set.create(option=current)
                watch.watchoption_set.create(option=runner_up)
                watch_result = watch.evaluate()
                watch.delete()

                [(unused_winrar, winrar_votes), (unused_luser, luser_votes)] = watch_result

                print u'{index}. {current.title} ({winrar_votes}-{luser_votes})'.format(**locals())

            index += 1
            last = category_result['order'][-1]

            print u'{index}. {last.title}'.format(**locals())

          print
