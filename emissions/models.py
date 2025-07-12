from djongo import models

class EmissionLog(models.Model):
    department = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    amount = models.FloatField()
    unit = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.department} - {self.amount} {self.unit}"
