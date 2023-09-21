from django.urls import path, reverse
from . import views
from django.contrib.auth.decorators import login_required, permission_required

is_staff_dec = permission_required('app_management.is_staff',login_url="/log-in")

urlpatterns = [
    path("", view=is_staff_dec(views.HomeView.as_view()), name="home-management"),
    path("add-artist", is_staff_dec(views.NewArtistView.as_view()), name="add-artist"),
    path("new-add-album", is_staff_dec(views.NewAlbumView.as_view()), name="add-album"),
    path("session-update", view=login_required(views.SessionUpdate.as_view()), name="session-update"),
    path("register", view=views.NewUserView.as_view(), name="register"),
    path("edit-artist/<int:pk>", is_staff_dec(views.EditArtist.as_view()), name="edit-artist"),
    path("edit-album/<int:pk>", is_staff_dec(views.EditAlbum.as_view()), name="edit-album"),
    path("edit-member/<int:pk>", is_staff_dec(views.EditMember.as_view()), name="edit-member"),
    path("add-a-rate", view=login_required(views.VoteCollector.as_view(),login_url="/log-in"), name="rate-album"),
    path("lote", is_staff_dec(views.ArtistChecker.as_view()), name="artist-checher"),
    path("add-role", is_staff_dec(views.AddRole.as_view()), name="add-role"),
    path("add-member", is_staff_dec(views.AddMember.as_view()), name="add-member"), 
    path("add-contribution/<int:pk>", is_staff_dec(views.AddContribution.as_view()), name="add-contrib"),
    path("choose-artist", view=is_staff_dec(views.SelectArtist.as_view()), name="choose-artist")
]
