from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    api_id = models.IntegerField()
    sprite_url = models.URLField()
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()

    def __str__(self):
        return self.name
