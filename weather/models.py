from django.db import models


class WeatherData(models.Model):
    city = models.CharField(max_length=100, db_index=True)
    temperature = models.FloatField()
    humidity = models.PositiveSmallIntegerField()
    wind_speed = models.FloatField()
    description = models.CharField(max_length=255, blank=True, null=True)
    pressure = models.IntegerField(blank=True, null=True)
    feels_like = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.city} ({self.timestamp.strftime('%Y-%m-%d %H:%M')}): {self.temperature}°C, {self.humidity}%"
