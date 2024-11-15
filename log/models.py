from django.db import models

# Create your models here.

class Trip(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    theme = models.CharField(max_length=50)  # Adventure, Relaxation, etc.
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='trip_photos/', blank=True, null=True)

    def __str__(self):
        return self.title

class Entry(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='entry_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.trip.title}"