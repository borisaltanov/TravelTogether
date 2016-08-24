from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

phone_regex = RegexValidator(regex=r'^\+359?\d{9}$',
                             message='Phone number must be entered' +
                             'in the format: +359XXXXXXXXX')


class Account(models.Model):
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, related_name='account',
        primary_key=True)
    phone = models.CharField(
        default='+359', validators=[phone_regex, ], max_length=13)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender='auth.User')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender='auth.User')
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()
