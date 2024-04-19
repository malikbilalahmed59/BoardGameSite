from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser  # Move this import here
from django.utils import timezone

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)


class Game(models.Model):
    cafe = models.ForeignKey('Cafe', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    time = models.DateTimeField()
    available_slots = models.IntegerField(default=0)
    # Add field to store ratings
    average_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    total_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()

class Cafe(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Cafe Name")
    description = models.TextField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    image = models.ImageField(upload_to='cafe_images/', blank=True, null=True, verbose_name="Cafe Image")


    def __str__(self):
        return self.name


class GameReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)