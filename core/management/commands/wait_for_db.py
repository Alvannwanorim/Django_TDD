"""
Django command to wait for database connection
"""

from django.core.management.base import baseCommand


class Command(baseCommand):
    """ Django command to wait for database"""

    def handle(self, *args, **options):
        pass
