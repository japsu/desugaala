from collections import defaultdict

from django.db import models

from vote.models import Category, Option

class Watch(models.Model):
  category = models.ForeignKey(Category)

  def evaluate(self):
    results = dict((wo.option, 0) for wo in self.watchoption_set.all())

    for ballot_category in self.category.ballotcategory_set.all():
      for ballot_option in ballot_category.ballotoption_set.all().order_by('order'):
        if self.watchoption_set.filter(option=ballot_option.option):
          results[ballot_option.option] += 1
          break

    results = list(i for i in results.iteritems())
    results.sort(key=lambda (option, num_votes): -num_votes)
    return results

  def __unicode__(self):
    options = u" vs. ".join(i.option.title for i in self.watchoption_set.all())
    category = self.category.title if self.category else u"None"

    return u"{category}: {options}".format(**locals())

class WatchOption(models.Model):
  watch = models.ForeignKey(Watch)
  option = models.ForeignKey(Option)

  def __unicode__(self):
    return self.option.title if self.option else u"None"