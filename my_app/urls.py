from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.Home.as_view(), name="home"),
    path("albums", view=views.AlbumsList.as_view(), name="albums"),
    path("album/<int:pk>/<slug:artist_slug>/<slug:album_slug>", view=views.SingleAlbum.as_view(), name="album"),
    path("artists", view=views.ArtistList.as_view(), name="artists"),
    path("artist/<int:pk>/<slug:slug>", view=views.SingleArtist.as_view(), name="artist"),
    path("log-in", view=views.Login.as_view(), name="log-in"),
    path("log-out", view=views.Logout.as_view(), name="log-out"),
    path("profile/<int:pk>", view=views.UserView.as_view(), name="user-profile"),
    path("artist-member/<int:pk>/<slug:slug>", view=views.MemberView.as_view(), name="member"),
    path("all-groups-members", view=views.MemberList.as_view(), name="member-list")
]
