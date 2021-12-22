from django.db import models
from django.contrib import admin
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    room_code = models.CharField(max_length=8)
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

class BoardSquare(models.Model):
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
