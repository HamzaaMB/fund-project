import uuid
from django.db import models
from django.db.models import Sum

class Fund(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    strategy = models.CharField(max_length=100)
    aum = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    inception_date = models.DateField(null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def total_aum(cls, strategy=None):
        """Returns the total AUM, optionally filtered by strategy."""
        funds = cls.objects.all()
        if strategy:
            funds = funds.filter(strategy=strategy)
        return funds.aggregate(total=Sum('aum'))['total'] or 0
