from typing import List, Optional, Dict, Union
from django.shortcuts import get_list_or_404, get_object_or_404
from app_management.models import Artist, Album, MetalHead


def get_fav_artists(query_list: List[int]) -> List[Artist]:
    artist_to_get = [int(pk) for pk in query_list]
    fav_artist = get_list_or_404(Artist, pk__in=artist_to_get)
    return fav_artist


def get_rated_albums(user_id:int, limit: Optional[int] = None) -> List[Album]:
    user = get_object_or_404(MetalHead, pk=user_id)
    votes = list(user.votes.keys())
    albums_to_get = None
    if limit:
        albums_to_get = [int(album_id) for album_id in votes[0:limit]]
    else:
        albums_to_get =[int(album_id) for album_id in votes]
    rated_albums = get_list_or_404(Album, pk__in=albums_to_get)
    return rated_albums


def rate_req_cleaner(query_dict: Dict[str, list]) -> Dict[str, Union[int, float]]:
    dict_to_return = {}
    for key, value in query_dict.items():
        match (key ==  "csrfmiddlewaretoken", key == "rate"):
            case (False, False):
                dict_to_return[key] = int(value)
            case (False, True):
                dict_to_return[key] = float(value)
            case _:
                pass
    return dict_to_return


def update_album_rating(album: Album, rating: float, new: bool,
                        add: bool = True, delete: bool = False):
    if add:
        if new:
            album.n_votes += 1
        album.rating += rating
    else:
        if delete:
            album.n_votes -= 1
        album.rating -= rating
    album.save()


def get_old_vote(user:MetalHead, album_id: int) -> float:
    return user.votes[str(album_id)]



def artist_name_exist(name: str) -> bool:
    pk = None
    try:
        if Artist.objects.get(name=name):
            pk = Artist.objects.get(name=name).pk
    except:
        pass
    return pk 
