from django.db import models
from datetime import datetime
from django.contrib import admin
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1000)
    profile_image = models.ImageField(upload_to ='uploads/% Y/% m/% d/')
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Game(models.Model):
    room_code = models.CharField(max_length=100)
    game_creater = models.IntegerField()
    game_opponent = models.IntegerField(blank=True, null=True)
    is_over = models.BooleanField(default=False)
    PLAYER_CHOICES = [
        ('R', 'Game Creator'),
        ('B', 'Game Opponent'),
        ('D', 'Draw'), 
        ('T', 'Terminated')
    ]
    won = models.CharField(max_length = 1, choices = PLAYER_CHOICES, blank=True, null=True)
    turn = models.BooleanField(default = True)
    red_score = models.IntegerField(default = 12, validators=[
        MaxValueValidator(12),
        MinValueValidator(0)
    ])
    black_score = models.IntegerField(default = 12, validators=[
        MaxValueValidator(12),
        MinValueValidator(0)
    ])
    creater_rating_change = models.IntegerField(default = 0)
    opponent_rating_change = models.IntegerField(default = 0)
    date = models.DateTimeField(default=datetime.now, blank=True)

class BoardSquare(models.Model):
    isKing = models.BooleanField(default = False)
    square_value = models.IntegerField(null = True)
    square_no = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(64)
    ])
    game = models.ForeignKey(Game, on_delete=CASCADE)



class FriendRequest(models.Model):
    friends = models.ManyToManyField(User,related_name="friends",blank=True)
    from_user = models.ForeignKey(User,related_name="from_user",on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name="to_user",on_delete=models.CASCADE)


admin.site.register(Game)
admin.site.register(FriendRequest)
admin.site.register(BoardSquare)
