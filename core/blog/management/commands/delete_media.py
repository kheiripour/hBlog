from django.core.management.base import BaseCommand
from os import listdir, remove
from os.path import isfile, join
from core import settings


class Command(BaseCommand):
    """
    Command for deleting media files.
    """

    def handle(self, *args, **options):
        media_path = join(settings.MEDIA_ROOT, "posts")
        for f in listdir(media_path):
            if isfile(join(media_path, f)):
                remove(join("/app/media/posts", f))
