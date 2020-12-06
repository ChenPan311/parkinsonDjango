from django.db import models

# Create your models here.

class UserModel(models.Model):
    username = models.CharField(max_length=30,verbose_name="אימייל")


    def __str__(self):
        return self.username
