from django.db import models


class Arrival(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    device_id = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Llegada {self.timestamp:%Y-%m-%d %H:%M:%S}"
