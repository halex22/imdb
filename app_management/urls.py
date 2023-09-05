from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home-management"),
    path("add-artist", view=views.NewArtistView.as_view(), name="add-artist"),
    path("new-add-album", view=views.NewAlbumView.as_view(), name="add-album"),
    path("session-update", view=views.SessionUpdate.as_view(), name="session-update"),
    path("register", view=views.NewUserView.as_view(), name="register"),
    path("edit-artist/<int:pk>", view=views.EditArtist.as_view(), name="edit-artist"),
    path("edit-album/<int:pk>", view=views.EditAlbum.as_view(), name="edit-album"),
    path("add-a-rate", view=views.VoteCollector.as_view(), name="rate-album"),
    path("lote", view=views.ArtistChecker.as_view(), name="artist-checher"),
    path("add-role", view=views.AddRole.as_view(), name="add-role"),
    path("add-member", view=views.AddMember.as_view(), name="add-member"),
    path("add-album-contrib", view=views.addContribAlbum.as_view(), name="add-album-contrib")
]
