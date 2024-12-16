from django.db import models

# Модель для описания артиста
class Artist(models.Model):
    name = models.CharField(max_length=100)  # Имя артиста
    country = models.CharField(max_length=100, blank=True)  # Страна артиста
    active_years = models.CharField(max_length=50, blank=True)  # Годы активности (например, "1960-1970")
    genre = models.CharField(max_length=50, blank=True)  # Жанр
    bio = models.TextField(blank=True)  # Биография артиста

    def __str__(self):
        return self.name

# Модель для описания альбома
class Album(models.Model):
    title = models.CharField(max_length=100)  # Название альбома
    release_date = models.DateField()  # Дата выхода альбома
    genre = models.CharField(max_length=50, blank=True)  # Жанр альбома
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    description = models.TextField(blank=True)  # Описание альбома

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

# Модель для описания трека
class Track(models.Model):
    title = models.CharField(max_length=100)  # Название трека
    duration = models.DurationField()  # Продолжительность трека
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    release_date = models.DateField(blank=True, null=True)  # Дата выхода трека
    description = models.TextField(blank=True)  # Описание трека

    def __str__(self):
        return f"{self.title} ({self.album.title})"
