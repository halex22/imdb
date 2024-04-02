from typing import Any, Dict

from django.contrib.auth import get_user_model, login
from django.forms.models import BaseModelForm
from django.http import (HttpRequest, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from my_metal_code import decorators
from my_metal_code.db_helper import artist_name_exist
from my_metal_code.decorators import (handle_img_from_form, presave_edit_form,
                                      show_errors, update_session)

from .forms import (ChoiceArtist, ContributionForm, MemberForm, NewArtistForm,
                    NewForm, RoleForm, SingUpForm)
from .models import Album, Artist, Contributions, Member, Role

User = get_user_model()

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


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
    template_name = "add/add_artist.html"
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
    template_name = "add/add_user.html"
    model = User
    form_class = SingUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class EditMember(UpdateView):
    template_name = "edit/edit_member.html"
    model = Member
    form_class = MemberForm

    @presave_edit_form()
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print(self.request.POST)
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        member = self.get_object()
        return reverse("member", args=[member.pk, member.slug])

class EditArtist(UpdateView):
    template_name = "edit_artist.html"
    model = Artist
    form_class = NewArtistForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)

    @presave_edit_form()
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        artist = self.get_object()
        return reverse("artist", args=[artist.pk, artist.slug])
    

class EditAlbum(UpdateView):
    template_name = "edit_album.html"
    model = Album
    form_class = NewForm
    success_url = reverse_lazy("album")

    @presave_edit_form()
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        album = self.get_object()
        return reverse("album", args=[album.pk, album.artist.slug, album.slug])


class VoteCollector(View):

    @decorators.rate_album
    def post(self, *args, **kwargs):
        album = get_object_or_404(Album, pk=int(self.request.POST["album_id"]))
        return redirect("album", pk=album.pk,
                        artist_slug=album.artist.slug,
                        album_slug = album.slug) # artist_slug, album_slug
    

class ArtistChecker(View):

    def post(self,*args, **kwargs):
        artist_id =  artist_name_exist(name=self.request.POST["artist_name"].lower())
        return JsonResponse({"message": artist_id})
    

class AddRole(CreateView):
    template_name = "add/add_role.html"
    model = Role
    form_class = RoleForm
    success_url = reverse_lazy("home")


class AddMember(CreateView):
    template_name = "add/add_member.html"
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("home")


class AddContribution(CreateView):
    template_name = "add/add_album_contrib.html"
    model = Contributions
    form_class = ContributionForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super(AddContribution, self).get_form_kwargs()
        kwargs["artist_id"] = self.request.get_full_path().split("/")[-1:][0]
        return kwargs
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)


class SelectArtist(FormView):
    template_name = "choose_artist.html"
    form_class = ChoiceArtist

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return redirect("add-contrib", pk=int(self.request.POST["artist"]))
    
