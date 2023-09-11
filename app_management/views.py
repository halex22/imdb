from typing import Any, Dict
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import TemplateView
from .forms import NewForm, NewArtistForm, SingUpForm, RoleForm, MemberForm, ContributionForm, choiceArtist
from .models import Artist, Album, Role, Member, Contributions
from my_metal_code.decorators import show_errors, handle_img_from_form, update_session, presave_edit_form
from my_metal_code import decorators
from django.contrib.auth import login
from django.urls import reverse_lazy
from my_metal_code.db_helper import artist_name_exist
from django.contrib.auth import get_user_model

User = get_user_model()

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
        return reverse("member", args=[int(self.get_object().pk)])

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
    

class VoteCollector(View):

    @decorators.rate_album
    def post(self, *args, **kwargs):
        return redirect("album", pk=int(self.request.POST["album_id"]))
    

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
    form_class = choiceArtist

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return redirect("add-contrib", pk=int(self.request.POST["artist"]))
    
