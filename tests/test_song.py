from flask import url_for


def test_get_songs(client):
    songs_url = url_for('app_song.song_list')
    rep = client.get(songs_url)
    assert rep.status_code == 200
