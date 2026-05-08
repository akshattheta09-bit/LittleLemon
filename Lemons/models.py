from django.db import models

class Reservation(models.Model):
    FIRST_NAME_MAX_LENGTH = 100
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    reservation_date = models.DateField()
    # We'll define time slots as choices. You can adjust these as needed.
    TIME_SLOTS = [
        ('19:00', '7:00 PM'),
        ('19:30', '7:30 PM'),
        ('20:00', '8:00 PM'),
        ('20:30', '8:30 PM'),
        ('21:00', '9:00 PM'),
        ('21:30', '9:30 PM'),
    ]
    reservation_slot = models.CharField(max_length=5, choices=TIME_SLOTS)

    class Meta:
        unique_together = ('reservation_date', 'reservation_slot')

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} at {self.reservation_slot}"
