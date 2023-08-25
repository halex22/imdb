from typing import Any, Dict, Mapping, Optional, Type, Union
from django.forms import Form, NumberInput, ModelForm
from django.forms.widgets import TextInput, Select, Input, SelectMultiple, ClearableFileInput, PasswordInput, EmailInput
from my_metal_code.subgenres import metal_subgenres
from .models import Artist, Album
from django.contrib.auth.models import User


class NewForm(ModelForm):
    class Meta:
        query_set = [(artist.name, artist.name) for artist in Artist.objects.all()]
        model = Album
        # fields = "__all__"
        exclude = ["added_date"]
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
        model = User
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
