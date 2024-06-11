from django.db import models


class TwoStepLogin(models.Model):
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    token = models.UUIDField()
    valid_until = models.DateTimeField()
