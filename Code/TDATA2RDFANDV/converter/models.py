from django.db import models

# Create your models here.


class downlEPW(models.Model):
    data = models.CharField(max_length=50, null=False, blank=False)