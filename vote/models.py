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
    user_agent = models.CharField(max_length=256)
    timestamp = models.DateTimeField()

class BallotOption(models.Model):
    order = models.IntegerField()
    ballot = models.ForeignKey(Ballot)
    option = models.ForeignKey(Option)

class AlreadyVoted(models.Model):
    userid = models.IntegerField(unique=True)

