from django import forms
from .models import Artist, Album, Track

# Форма для добавления артиста
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre', 'bio']

# Форма для добавления альбома
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'release_date', 'artist']

# Форма для добавления трека
class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'duration', 'album']
