from django.db import models
from django.contrib import admin
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator
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

class Player(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

admin.site.register(Game)
admin.site.register(BoardSquare)
admin.site.register(Player)