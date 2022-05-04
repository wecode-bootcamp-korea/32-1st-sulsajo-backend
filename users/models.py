from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel):
    email      = models.CharField(max_length=100, unique=True)
    password   = models.CharField(max_length=200)
    name       = models.CharField(max_length=30)
    nick_name  = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'users'