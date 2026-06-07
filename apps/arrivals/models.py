from django.db import models


class Arrival(models.Model):
    ENTER = 'enter'
    EXIT = 'exit'
    EVENT_CHOICES = [(ENTER, 'Entrada'), (EXIT, 'Salida')]

    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    device_id = models.CharField(max_length=100, blank=True, default='')
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES, default=ENTER)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        label = 'Entrada' if self.event_type == self.ENTER else 'Salida'
        return f"{label} {self.timestamp:%Y-%m-%d %H:%M:%S}"
