from django.db import models
from django.utils import timezone
from django.core.validators import ValidationError


def date_validation(date):
    if date <= timezone.now():
        raise ValidationError(u'{} is in the past!'.format(date))


SEAT_CHOICES = [(s, s) for s in range(1, 13)]

with open('travels/towns.txt') as infile:
    towns = infile.read().splitlines()

TOWNS = [(town, town) for town in towns]


class Travel(models.Model):
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    depart_time = models.DateTimeField(validators=[date_validation, ])
    start = models.CharField(max_length=20, choices=TOWNS)
    end = models.CharField(max_length=20, choices=TOWNS)
    free_seats = models.PositiveSmallIntegerField(default=1)
    fee = models.PositiveSmallIntegerField(default=1)
    duration = models.CharField(max_length=20, default='')
    distance = models.CharField(max_length=20, default='')

    class Meta:
        db_table = 'Travel'

    def __str__(self):
        return '{}-{} at {}'.format(self.start, self.end, self.depart_time)

    def get_depart_time(self):
        return self.depart_time


class TravelRegister(models.Model):
    travel = models.ForeignKey(Travel)
    user = models.ForeignKey('auth.User')

    def __str__(self):
        return '{}-{}'.format(self.travel, self.user)
