from django.db import models

# Create your models here.
class Register(models.Model):
    fname = models.TextField()
    lname = models.TextField()
