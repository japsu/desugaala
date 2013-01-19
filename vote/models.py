from django.db import models

from pyvotecore.schulze_method import SchulzeMethod

class Category(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024, default='', blank=True)

    def evaluate(self):
        category_input = []

        for ballot_category in self.ballotcategory_set.all():
            ballot_options = ballot_category.ballotoption_set.all().order_by('order')
            category_input.append(dict(
                count=1,
                ballot=[[ballot_option.option] for ballot_option in ballot_options]
            ))

        if category_input:
            category_result = SchulzeMethod(category_input, ballot_notation='grouping').as_dict()
        else:
            category_result = dict()

        return category_result

    def __unicode__(self):
        return self.title

class Option(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.title

class Ballot(models.Model):
    ip_address = models.CharField(max_length=16)
    user_agent = models.CharField(max_length=256)
    timestamp = models.DateTimeField()

class BallotCategory(models.Model):
    ballot = models.ForeignKey(Ballot)
    category = models.ForeignKey(Category)

class BallotOption(models.Model):
    order = models.IntegerField()
    ballot_category = models.ForeignKey(BallotCategory)
    option = models.ForeignKey(Option)

class AlreadyVoted(models.Model):
    user_id = models.IntegerField(unique=True)
    ip_address = models.CharField(max_length=16)
    user_agent = models.CharField(max_length=256)
    timestamp = models.DateTimeField()
