from typing import Dict, List, Union

from django.db.models.query import QuerySet
from django.forms.widgets import Select, SelectMultiple


def capitalize_words(name: str) -> str:
    words = [word.capitalize() for word in name.split(" ")]
    cap_name = " ".join(words)
    return cap_name


def create_select(iterable: Union[QuerySet, List[str]], attrs:Dict[str,str] = None) -> Select:
    if not attrs:
        default_attrs = {"class": "form-element form-select"}
    widget = Select(
        attrs=default_attrs,
        choices = [(item.id if isinstance(iterable, QuerySet) else item,
                    capitalize_words(str(item))) for item in iterable]
    )
    return widget


def create_multi_select(iterable: Union[QuerySet, List[str]], attrs:Dict[str,str] = None) -> SelectMultiple:
    if not attrs:
        default_attrs = {"class": "form-select"}
    widget = SelectMultiple(
        attrs=default_attrs,
        choices = [(item.id if isinstance(iterable, QuerySet) else item,
                    capitalize_words(str(item))) for item in iterable]
    )
    return widget