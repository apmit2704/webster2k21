from django.db import models
from django.contrib import admin

# Create your models here.

class Game(models.Model):
    room_code = models.CharField(max_length=100)
    game_creater = models.IntegerField()
    game_opponent = models.IntegerField(blank=True, null=True)
    is_over = models.BooleanField(default=False)

admin.site.register(Game)