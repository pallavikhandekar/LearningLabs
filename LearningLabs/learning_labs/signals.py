__author__ = 'nimmicv'

from django.db.models.signals import pre_save
from django.dispatch import receiver
from learning_labs.models import Answers

@receiver(pre_save, sender=Answers)
def my_handler(sender, **kwargs):
    print sender