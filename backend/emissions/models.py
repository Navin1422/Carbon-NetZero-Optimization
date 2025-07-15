from djongo import models
from bson import ObjectId

class Department(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EmissionLog(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='emission_logs')
    source = models.CharField(max_length=100)   # e.g., "Boiler"
    amount = models.FloatField()                # e.g., 120.5
    unit = models.CharField(max_length=20)      # e.g., "kg"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.department.name} - {self.amount} {self.unit}"

