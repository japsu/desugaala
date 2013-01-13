from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=64)

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
    userid = models.IntegerField(unique=True)
    ip_address = models.CharField(max_length=16)
    user_agent = models.CharField(max_length=256)
    timestamp = models.DateTimeField()
