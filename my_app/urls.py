from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.Home.as_view(), name="home"),
    path("albums", view=views.AlbumsList.as_view(), name="albums"),
    path("album/<int:pk>", view=views.SingleAlbum.as_view(), name="album"),
    path("artists", view=views.ArtistList.as_view(), name="artists"),
    path("artist/<int:pk>", view=views.SingleArtist.as_view(), name="artist"),
    path("log-in", view=views.Login.as_view(), name="log-in"),
    path("log-out", view=views.Logout.as_view(), name="log-out"),
    path("profile/<int:pk>", view=views.UserView.as_view(), name="user-profile")
]
