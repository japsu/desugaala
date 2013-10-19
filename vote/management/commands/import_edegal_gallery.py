import requests

from django.core.management.base import BaseCommand, CommandError

from vote.models import Category, Option, OptionPicture

def epsilonator(target):
    def epsilon(media):
        return abs(media['width'] - target)

    return epsilon

thumbnail_epsilon = epsilonator(120)
preview_epsilon = epsilonator(600)

class Command(BaseCommand):
    args = 'http://gallery.example.com/v2/path/to/album'
    help = 'Import an Edegal gallery as an album into the voting application'

    def handle(*args, **options):
        for album_url in args[1:]:
          base_url, unused = album_url.split('/v2/', 1)
          album = requests.get(album_url).json()

          category = Category.objects.create(
              title=album['title'],
              description=album['description'],
              template='category_picture.jade'
          )

          for picture in album['pictures']:
              if '-00' in picture['title']:
                continue
                
              option = category.option_set.create(title=picture['title'])

              thumbnail = min(picture['media'], key=thumbnail_epsilon)
              preview = min(picture['media'], key=preview_epsilon)

              OptionPicture.objects.create(
                  option=option,
                  thumbnail=base_url + thumbnail['src'],
                  preview=base_url + preview['src'],
                  link=base_url + picture['path']
              )

