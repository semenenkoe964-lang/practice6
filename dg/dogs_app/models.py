from django.db import models


class DogBreed(models.Model):
    """Модель для хранения информации о породах собак"""
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DogImage(models.Model):
    """Модель для хранения ссылок на изображения собак"""
    breed = models.CharField(max_length=100)
    image_url = models.URLField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.breed} image"
