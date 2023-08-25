from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import BaseModelForm
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from .forms import NewForm, NewArtistForm
from .models import Artist, Album
from django.contrib.auth.models import User
from my_metal_code.decorators import show_errors, handle_img_from_form, update_session, presave_edit_form
from django.contrib.auth import login
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = "index.html"


class NewAlbumView(CreateView):
    template_name = "add_album.html"
    form_class = NewForm
    model = Album
    success_url = "/app-management"

    @show_errors
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @handle_img_from_form
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)


class NewArtistView(CreateView):
    template_name = "add_artist.html"
    model = Artist
    form_class = NewArtistForm
    success_url = "/app-management"

    @show_errors
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    @handle_img_from_form
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)


class SessionUpdate(View):

    @update_session(session_name="fav_artists", query_name="artist_info")
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        return JsonResponse({"message": "Session data updated successfully."})


class NewUserView(CreateView):
    template_name = "add_user.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
    

class EditArtist(UpdateView):
    template_name = "edit_artist.html"
    model = Artist
    form_class = NewArtistForm

    @presave_edit_form()
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("artist", args=[int(self.get_object().pk)])
    

class EditAlbum(UpdateView):
    template_name = "edit_album.html"
    model = Album
    form_class = NewForm
    success_url = reverse_lazy("album")

    @presave_edit_form()
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse("album", args=[int(self.get_object().pk)])