from typing import Any, Dict, Mapping, Optional, Type, Union, Iterable
from django.forms import Form, NumberInput, ModelForm, FloatField, IntegerField, ModelChoiceField
from django.forms.widgets import TextInput, Select, Input, SelectMultiple, ClearableFileInput, PasswordInput, EmailInput
from my_metal_code.choices_lists import metal_subgenres, metal_instruments
from my_metal_code.forms_helper import create_select, create_multi_select
from .models import Artist, Album, MetalHead, Role, Member, Contributions, Genre
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()


class choiceArtist(Form):
    artist = ModelChoiceField(
        queryset=Artist.objects,
        widget=Select(attrs={"class": "form-element form-select"})
    )


class SingUpForm(UserCreationForm):
    
    class Meta:
       model = User
       fields = ("username",)
       field_classes = {"username": UsernameField}


class NewForm(ModelForm):
    class Meta:
        model = Album
        # fields = "__all__"
        exclude = ["added_date", "n_votes", "rating", "slug"]
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
            "artist": create_select(iterable=Artist.objects.all())
        }
        error_messages = {
            "album_name": {
                "required": "album name can not be empty"
            }
        }


class NewArtistForm(ModelForm):
    class Meta:
        query_set = Genre.objects.all()
        model = Artist
        fields = "__all__"
        exclude = ["added_date", "slug", "subgenres"]

        labels = {
            "name": "Band Name",
            "genre": "Main Genre",
            "fundation_date": "Fundation Year",
            "img": "Band Image",
            "active_members": "Active Members",
            "all_members": "All Members",
            "genres": "Band Genres"
        }

        widgets = {
            "fundation_date": NumberInput(),
            # "genre":create_select(iterable=metal_subgenres),
            "subgenres": create_multi_select(iterable=metal_subgenres),
            "img": ClearableFileInput(attrs={"accept": "image/*"}),  # Add this line for the file input
            "genres": create_multi_select(iterable=query_set)
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

    class Meta:
        model =  Role
        fields = "__all__"

        widgets = {
            "name": create_select(iterable=metal_instruments)
        }

        help_text =  {
            "Guitarrist, Drummer, Singer... if the role is not on the list please contact one of the admin members"
        }


class MemberForm(ModelForm):

    class Meta:
        model = Member
        fields = "__all__"
        exclude = ["slug"]
        text_widget = TextInput(attrs={"class": "form-element"})
        select_widget = create_multi_select(iterable=Artist.objects.all())
        labels = {"birth_date": "Date of Birth", "active_on": "Current active on"}

        widgets = {
            "first_name": text_widget,
            "last_name": text_widget,
            "nickname": text_widget,
            "birth_date": Input(attrs={"class": "form-element", "type": "date"}),
            "active_on": select_widget,
            "former_on": select_widget,
        }


class ContributionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        artist_id = kwargs.pop('artist_id')
        artist = Artist.objects.get(pk=int(artist_id))
        all_members = artist.former_groups.all().union(artist.active_groups.all())
        super(ContributionForm, self).__init__(*args, **kwargs)
        self.fields["member"].widget = create_select(iterable=all_members)
        self.fields["album"]. widget = create_select(iterable=artist.albums.all())

    class Meta:
        model = Contributions
        fields = "__all__"
        widgets = {"roles": create_multi_select(iterable=Role.objects.all())}
        