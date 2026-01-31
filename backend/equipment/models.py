from django.db import models

class Dataset(models.Model):
    filename = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    total_equipment = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"
