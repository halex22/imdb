from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home-management"),
    path("add-artist", view=views.NewArtistView.as_view(), name="add-artist"),
    path("new-add-album", view=views.NewAlbumView.as_view(), name="add-album"),
    path("session-update", view=views.SessionUpdate.as_view(), name="session-update"),
    path("register", view=views.NewUserView.as_view(), name="register"),
    path("edit-artist/<int:pk>", view=views.EditArtist.as_view(), name="edit-artist"),
    path("edit-album/<int:pk>", view=views.EditAlbum.as_view(), name="edit-album")
]
