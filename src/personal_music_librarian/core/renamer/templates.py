DEFAULT_TEMPLATES = {
    'artist_album_track': (
        '{albumartist}/{album}/'
        '{discnumber:02d}-{tracknumber:02d} {title}.flac'
    ),
    'artist_album_simple': (
        '{artist}/{album}/'
        '{tracknumber:02d} {title}.flac'
    ),
    'flat_library': (
        '{artist} - {title}.flac'
    ),
}
