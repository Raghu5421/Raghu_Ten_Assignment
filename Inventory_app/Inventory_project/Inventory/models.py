from django.db import models
from django.utils import timezone
import uuid

MAX_BOOKINGS = 2

class Inventory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    remaining_count = models.IntegerField()
    expiration_date = models.DateField()

    class Meta:
        db_table = 'inventory_table'

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    booking_count = models.IntegerField(default=0)
    date_joined = models.DateTimeField()

    class Meta:
        db_table = 'members_table'

    def __str__(self):
        return f"{self.name} {self.surname}"


class Booking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    reference = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        db_table = 'booking_table'

    def __str__(self):
        return f"Booking: {self.member.name} - {self.inventory.title} ({self.booking_date})"
