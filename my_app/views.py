from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView

from app_management.forms import RatingForm
from app_management.models import Album, Artist, Member
from my_metal_code.db_helper import get_fav_artists, get_rated_albums
from my_metal_code.query_filters import QueryManager

User = get_user_model()

class Home(TemplateView):
    template_name = "my_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user        
        context["message"] = messages.get_messages(self.request)
        if self.request.user.is_authenticated:
            if "fav_artists" in self.request.session:
                context["fav_artists"] = get_fav_artists(self.request.session["fav_artists"])
        context["latest_artist"] = Artist.objects.all().order_by("-added_date")[:3]
        context["latest_albums"] = Album.objects.all().order_by("-added_date")[:3]
        context["latest_members"] = Member.objects.all().order_by("-pk")[:3]
        return context
    

class AlbumsList(TemplateView):
    template_name = "my_app/album_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alphabet_order"] = True
        if self.request.GET:
            query = QueryManager(self.request.GET.copy(), context, Album)
            query.update_context()
            return query.context
        context["albums"] = Album.objects.all()
        return context
    

class SingleAlbum(DetailView):
    template_name = "my_app/album.html"
    model = Album

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = RatingForm()
        context["message"] = messages.get_messages(self.request)
        return context


class ArtistList(TemplateView):
    template_name = "my_app/artist_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            query = QueryManager(self.request.GET.copy(), context, Artist)
            query.update_context()
            return query.context
        context["artists"] = Artist.objects.all()
        return context


class SingleArtist(DetailView):
    template_name = "my_app/artist.html"
    model = Artist

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        artist = self.get_object() 
        if "fav_artists" in self.request.session:
            fav_artist = [int(_) for _ in self.request.session["fav_artists"]]
            context["is_favorite"] = artist.id in fav_artist
        context["user"] = self.request.user
        return context
    

class Login(LoginView):
    template_name = "my_app/registration/log_in.html"
    redirect_authenticated_user = True

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        messages.success(self.request, "Successfully logged in. We glad to see you again !")
        return super().form_valid(form)

    def get_redirect_url(self) -> str:
        return reverse_lazy("home")


class Logout(LogoutView):

    def get_redirect_url(self) -> str:
        return reverse_lazy("home")
    

class UserView(DetailView):
    template_name = "my_app/user_profile.html"
    model = User
    context_object_name = "metalhead"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        metalhead = self.get_object()
        if self.request.session.get("fav_artists"):
            context["fav_artists"] = get_fav_artists(self.request.session.get("fav_artists"))
        if metalhead.votes:
            context["rated_albums"] = get_rated_albums(user_id=int(metalhead.pk))
        return context
    

class MemberView(DetailView):
    template_name = "my_app/show_member.html"
    model = Member
    context_object_name = "member"


class MemberList(TemplateView):
    template_name = "my_app/member_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            query = QueryManager(self.request.GET.copy(), context, Member)
            query.update_context()
            return query.context
        context["members"] = Member.objects.all()
        return context
        