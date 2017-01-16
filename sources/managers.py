from random import randint

from django.db import models
from django.db.models.aggregates import Count


class RandomManager(models.Manager):
    """
    Custom manager class, adds random() method which returns a single random item to the Manager class
    """

    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]