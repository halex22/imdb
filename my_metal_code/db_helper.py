from typing import List, Union
from django.shortcuts import get_list_or_404
from app_management.models import Artist


def get_fav_artists(query_list: List[int]) -> List[Artist]:
    artist_to_get = [int(pk) for pk in query_list]
    fav_artist = get_list_or_404(Artist, pk__in=artist_to_get)
    return fav_artist