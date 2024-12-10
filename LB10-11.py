from flask import Flask, request, jsonify, send_file, render_template
import xml.etree.ElementTree as ET
import os
import json

app = Flask(__name__)

# Пути к XML-файлам
ARTISTS_FILE = "artists.xml"
ALBUMS_FILE = "albums.xml"
TRACKS_FILE = "tracks.xml"

# Инициализация XML-файлов
def initialize_xml_files():
    for file in [ARTISTS_FILE, ALBUMS_FILE, TRACKS_FILE]:
        if not os.path.exists(file):
            root = ET.Element(file.split('.')[0])
            tree = ET.ElementTree(root)
            tree.write(file, encoding="utf-8", xml_declaration=True)

# Чтение данных из XML-файла
def read_from_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for element in root:
            item = {child.tag: child.text for child in element}
            data.append(item)
        return data
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# Запись данных в XML-файл
def write_to_xml(file_path, data):
    root = ET.Element(file_path.split('.')[0])
    for record in data:
        element = ET.SubElement(root, root.tag[:-1])
        for key, value in record.items():
            ET.SubElement(element, key).text = value
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# Экспорт данных в JSON
@app.route('/export_json', methods=['GET'])
def export_to_json():
    all_data = {
        "artists": read_from_xml(ARTISTS_FILE),
        "albums": read_from_xml(ALBUMS_FILE),
        "tracks": read_from_xml(TRACKS_FILE)
    }
    with open("exported_data.json", "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, indent=4, ensure_ascii=False)
    return send_file("exported_data.json", as_attachment=True)

# Импорт данных из JSON
@app.route('/import_json', methods=['POST'])
def import_from_json():
    file = request.files.get('file')
    if not file or file.filename == '':
        return "No file provided!", 400

    try:
        data = json.load(file)
    except json.JSONDecodeError as e:
        return f"Invalid JSON file: {e}", 400

    # Чтение существующих данных
    existing_artists = read_from_xml(ARTISTS_FILE)
    new_artists = data.get("artists", [])

    # Объединение данных
    combined_artists = existing_artists + [
        artist for artist in new_artists if artist not in existing_artists
    ]

    write_to_xml(ARTISTS_FILE, combined_artists)

    # Повторяем логику для albums и tracks
    existing_albums = read_from_xml(ALBUMS_FILE)
    new_albums = data.get("albums", [])
    combined_albums = existing_albums + new_albums
    write_to_xml(ALBUMS_FILE, combined_albums)

    existing_tracks = read_from_xml(TRACKS_FILE)
    new_tracks = data.get("tracks", [])
    combined_tracks = existing_tracks + new_tracks
    write_to_xml(TRACKS_FILE, combined_tracks)

    return "Data imported successfully!"

    # Обработка данных
    for table_name, file_path in [
        ("artists", ARTISTS_FILE),
        ("albums", ALBUMS_FILE),
        ("tracks", TRACKS_FILE)
    ]:
        if table_name in data:
            write_to_xml(file_path, data[table_name])
    return "Data imported successfully!"


# Добавление артиста
@app.route('/add_artist', methods=['POST'])
def add_artist():
    name = request.form.get('name')
    genre = request.form.get('genre')
    country = request.form.get('country')
    if not all([name, genre, country]):
        return "All fields are required!", 400
    artists = read_from_xml(ARTISTS_FILE)
    new_id = str(len(artists) + 1)
    new_artist = {"ID": new_id, "Name": name, "Genre": genre, "Country": country}
    artists.append(new_artist)
    write_to_xml(ARTISTS_FILE, artists)
    return f"Artist '{name}' added successfully!"
# Добавление альбома
@app.route('/add_album', methods=['POST'])
def add_album():
    title = request.form.get('title')
    release_year = request.form.get('release_year')
    artist_id = request.form.get('artist_id')
    if not all([title, release_year, artist_id]):
        return "All fields are required!", 400
    albums = read_from_xml(ALBUMS_FILE)
    new_id = str(len(albums) + 1)
    new_album = {"ID": new_id, "Title": title, "ReleaseYear": release_year, "ArtistID": artist_id}
    albums.append(new_album)
    write_to_xml(ALBUMS_FILE, albums)
    return f"Album '{title}' added successfully!"

# Добавление трека
@app.route('/add_track', methods=['POST'])
def add_track():
    title = request.form.get('title')
    duration = request.form.get('duration')
    album_id = request.form.get('album_id')
    if not all([title, duration, album_id]):
        return "All fields are required!", 400
    tracks = read_from_xml(TRACKS_FILE)
    new_id = str(len(tracks) + 1)
    new_track = {"ID": new_id, "Title": title, "Duration": duration, "AlbumID": album_id}
    tracks.append(new_track)
    write_to_xml(TRACKS_FILE, tracks)
    return f"Track '{title}' added successfully!"


# Просмотр данных
@app.route('/view_artists')
def view_artists():
    artists = read_from_xml(ARTISTS_FILE)
    return jsonify(artists)

@app.route('/view_albums')
def view_albums():
    albums = read_from_xml(ALBUMS_FILE)
    return jsonify(albums)

@app.route('/view_tracks')
def view_tracks():
    tracks = read_from_xml(TRACKS_FILE)
    return jsonify(tracks)

if __name__ == '__main__':
    initialize_xml_files()
    app.run(debug=True)
