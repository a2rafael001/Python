from django.contrib import admin
from .models import Artist, Album, Track

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')
    search_fields = ('name', 'genre')
    list_filter = ('genre',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'artist')
    search_fields = ('title',)
    list_filter = ('release_date',)

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'duration')
    search_fields = ('title',)
