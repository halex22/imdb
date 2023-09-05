from typing import Any, Dict, Mapping, Optional, Type, Union
from django.forms import Form, NumberInput, ModelForm, FloatField, IntegerField
from django.forms.widgets import TextInput, Select, Input, SelectMultiple, ClearableFileInput, PasswordInput, EmailInput
from my_metal_code.choices_lists import metal_subgenres, metal_instruments
from .models import Artist, Album, MetalHead, Role, Member, AlbumContributor
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()

class SingUpForm(UserCreationForm):
    
    class Meta:
       model = User
       fields = ("username",)
       field_classes = {"username": UsernameField}


class NewForm(ModelForm):
    class Meta:
        query_set = [(artist.name, artist.name) for artist in Artist.objects.all()]
        model = Album
        # fields = "__all__"
        exclude = ["added_date", "n_votes", "rating"]
        labels = {
            "name": "Name of the album",
            "img": "Album cover"
        }
        widgets = {
            "name": TextInput(attrs={"class": "form-element"}),
            "released_date": Input(
                attrs={
                    "class": "form-element",
                    "type": "date"
                },
            ),
            "artist": Select(attrs={"class": "form-element form-select"},
                             choices=query_set)
        }
        error_messages = {
            "album_name": {
                "required": "album name can not be empty"
            }
        }


class NewArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = "__all__"
        exclude = ["added_date"]

        labels = {
            "name": "Band Name",
            "genre": "Main Genre",
            "fundation_date": "Fundation Year",
            "img": "Band Image"
        }

        widgets = {
            "fundation_date": NumberInput(),
            "subgenres": SelectMultiple(
                attrs={"class": "form-select"},
                choices=[(genre, genre) for genre in metal_subgenres]
            ),
            "img": ClearableFileInput(attrs={"accept": "image/*"}),  # Add this line for the file input
        }


class NewUserForm(ModelForm):
    class Meta:
        model = MetalHead
        fields = ["username", "email", "password"]

        widgets = {
            "password": PasswordInput(attrs={"class": "password-field"})
        }

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        common_class = 'common-class'
        for field_name, field in self.fields.items():
            widget = field.widget
            if 'class' in widget.attrs:
                widget.attrs['class'] += f' {common_class}'
            else:
                widget.attrs['class'] = common_class


class RatingForm(Form):
    
    rating = FloatField(max_value=10, min_value=1, help_text="rate this album in the scale of 1 to 10")
    voter_id = IntegerField(min_value=1, required=True)
    album_id = IntegerField(min_value=1, required=True)


class RoleForm(ModelForm):

    added_roles = [role.name for role in Role.objects.all()]

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.added_roles = [role.name for role in Role.objects.all()]

    class Meta:
        model =  Role
        fields = "__all__"

        widgets = {
            "name": Select(
                attrs={"class": "form-element form-select"},
                choices= [(instrument, instrument) for instrument in metal_instruments]
            )
        }

        help_text =  {
            "Guitarrist, Drummer, Singer... if the role is not on the list please contact one of the admin members"
        }


class MemberForm(ModelForm):

    class Meta:
        model = Member
        fields = "__all__"
        
        labels = {
            "birth_date": "Date of Birth"
        }

        widgets = {
            "first_name": TextInput(attrs={"class": "form-element"}),
            "last_name": TextInput(attrs={"class": "form-element"}),
            "nickname": TextInput(attrs={"class": "form-element"}),
            "birth_date": Input(attrs={"class": "form-element", "type": "date"})
        }


class AlbumContributorForm(ModelForm):

    class Meta:
        model = AlbumContributor
        fields = "__all__"

        labels = {
            "role": "Contribution in this album"
        }

        widgets = {
            "member": Select(
                attrs={"class": "form-element form-select"},
                choices= [(member, member) for member in Member.objects.all()]
            ),
            "role": Select(
                attrs={"class": "form-element form-select"},
                choices=[(role, role) for role in Role.objects.all()]
            ),
            "album": Select(
                attrs={"class": "form-element form-select"},
                choices=[(album, album) for album in Album.objects.all()]
            )
        }

