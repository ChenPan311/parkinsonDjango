from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Doctor(models.Model):
    Office_Phone = models.CharField(max_length=20, verbose_name="טלפון משרדי")
    Mobile_Phone = models.IntegerField(default=0, verbose_name="טלפון נייד")
    Organization = models.CharField(max_length=128, blank=True,verbose_name="ארגון")

    def __str__(self):
        return self.user.username


class Patient (models.Model):
    # מס
    # פלאפון
    # ארץ
    # לידה
    # תאריך
    # לידה – חישוב
    # גיל
    # תז
    # מייל
    # שנות
    # השכלה
    # שם
    # קופת
    # חולים
    # שם
    # מרפאה
    Mobile_Phone = models.IntegerField(default=0, verbose_name="טלפון נייד")
    Country=models.CharField(max_length=20, verbose_name="ארץ לידה")
    HMO=models.CharField(max_length=20, verbose_name="קופת חולים")




