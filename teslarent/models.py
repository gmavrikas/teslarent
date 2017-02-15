import datetime
from django.db import models
from pytz import timezone


tz_utc = timezone('UTC')


class Credentials(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=200, unique=True)
    current_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    token_expires_at = models.DateTimeField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Credentials"


class Vehicle(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    linked = models.BooleanField('False if the credentials were removed or the vehicle is not listed anymore')
    id = models.BigIntegerField(primary_key=True)
    vehicle_id = models.BigIntegerField()
    credentials = models.ForeignKey(Credentials, on_delete=models.SET_NULL, default=None, blank=True, null=True,)
    display_name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    vin = models.CharField(max_length=17)
    state = models.CharField(max_length=200)

    @property
    def is_active(self):
        return self.linked and self.credentials is not None

    def __str__(self):
        return self.display_name + ' ' + self.vin + ' (' + str(self.credentials) + ')'


class Rental(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vehicle = models.ForeignKey(Vehicle)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(default=None, blank=True, null=True)
    code = models.UUIDField(unique=True)
    odometer_start = models.IntegerField(default=None, blank=True, null=True)
    odometer_end = models.IntegerField(default=None, blank=True, null=True)

    @property
    def is_active(self):
        now = tz_utc.localize(datetime.datetime.utcnow())
        return self.start <= now < self.end and self.vehicle.is_active

    @property
    def distance_driven(self):
        return self.odometer_end - self.odometer_start
