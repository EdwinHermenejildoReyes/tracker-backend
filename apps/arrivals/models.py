from django.db import models


class Arrival(models.Model):
    ENTER = 'enter'
    EXIT = 'exit'
    STATIONARY = 'stationary'
    STATIONARY_END = 'stationary_end'
    EVENT_CHOICES = [
        (ENTER, 'Entrada'),
        (EXIT, 'Salida'),
        (STATIONARY, 'Estacionario'),
        (STATIONARY_END, 'Fin estacionario'),
    ]

    event_id = models.UUIDField(unique=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    device_id = models.CharField(max_length=100, blank=True, default='')
    event_type = models.CharField(max_length=14, choices=EVENT_CHOICES, default=ENTER)
    duration_seconds = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    @property
    def duration_display(self):
        if self.duration_seconds is None:
            return None
        s = self.duration_seconds
        if s < 60:
            return f"{s}s"
        if s < 3600:
            return f"{s // 60}m {s % 60}s"
        return f"{s // 3600}h {(s % 3600) // 60}m"

    def __str__(self):
        label = 'Entrada' if self.event_type == self.ENTER else 'Salida'
        return f"{label} {self.timestamp:%Y-%m-%d %H:%M:%S}"
