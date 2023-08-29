from typing import List, Union
from django.shortcuts import get_list_or_404
from app_management.models import Artist, Album, MetalHead


def get_fav_artists(query_list: List[int]) -> List[Artist]:
    artist_to_get = [int(pk) for pk in query_list]
    fav_artist = get_list_or_404(Artist, pk__in=artist_to_get)
    return fav_artist

def rate_req_cleaner(queryDict: dict) -> dict:
    dict_to_return = {}
    for key, value in queryDict.items():
        match (key ==  "csrfmiddlewaretoken", key == "rate"):
            case (False, False):
                dict_to_return[key] = int(value[0])
            case (False, True):
                dict_to_return[key] = float(value[0])
            case _:
                pass
    return dict_to_return


def update_album_rating(album: Album, rating: float, add: bool = True):
    if album.n_votes >= 1:
        if add:
            album.n_votes += 1
            album.rating += rating
        else:
            album.n_votes -= 1
            album.rating -= rating
    if album.n_votes == 0:
        album.n_votes += 1
        album.rating += rating
    album.save()


def get_old_vote(user:MetalHead, album_id: int):
    return user.votes[str(album_id)]