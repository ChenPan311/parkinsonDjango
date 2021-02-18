from django.db import models
# Create your models here.

class Doctor(models.Model):
    office_phone = models.CharField(max_length=20, verbose_name="טלפון משרדי")
    mobile_phone = models.CharField(max_length=20, verbose_name="טלפון נייד")
    organization = models.CharField(max_length=128, blank=True, verbose_name="ארגון")

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    mobile_phone = models.CharField(max_length=20, verbose_name="טלפון נייד")
    country = models.CharField(max_length=20, verbose_name="ארץ לידה")

