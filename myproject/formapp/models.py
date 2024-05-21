from django.db import models
# from decimal import Decimal

class FormData(models.Model):
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=15, decimal_places=2)
    rate = models.DecimalField(max_digits=15, decimal_places=2)
    covlim = models.DecimalField(max_digits=15, decimal_places=2)
    minprem = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name