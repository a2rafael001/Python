from django.shortcuts import render, redirect
from .forms import ArtistForm, AlbumForm, TrackForm
from .models import Artist, Album, Track

# Главная страница
def home(request):
    artists = Artist.objects.all()
    albums = Album.objects.all()
    tracks = Track.objects.all()

    context = {
        'artists': artists,
        'albums': albums,
        'tracks': tracks,
    }
    return render(request, 'music/home.html', context)

# Добавление артиста
def add_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArtistForm()
    return render(request, 'music/add_artist.html', {'form': form})

# Добавление альбома
def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AlbumForm()
    return render(request, 'music/add_album.html', {'form': form})

# Добавление трека
def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TrackForm()
    return render(request, 'music/add_track.html', {'form': form})
