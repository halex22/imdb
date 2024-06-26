from functools import wraps

from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from app_management.models import Album, MetalHead

from .db_helper import get_old_vote, rate_req_cleaner, update_album_rating


def show_errors(view_method):
    """
    decorator function to be used with a view class like CreateView or EditView
    note: the view class must have a post method defind
    """

    def decorator(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            for field_name, errors in form.errors.items():
                for error_message in errors:
                    print(f"Error for field '{field_name}': {error_message}")
        return view_method(self, request, *args, **kwargs)

    return decorator


def handle_img_from_form(view_method):
    """
    decorator function to handle the storate og the image loaded in a form
    note: remember to name the field "img" to proceed properly
    """

    def decorator(self, form: BaseModelForm, *args, **kwargs):
        instance = form.save(commit=False)
        if "img" in self.request.FILES:
            instance.img = self.request.FILES["img"]
            instance.save()
            return view_method(self, form, *args, **kwargs)
        else:
            raise AttributeError("The 'img' field is missing in the form.")

    return decorator

def adjust_edit_form(view_method):
    def decorator(self, request: HttpRequest, *args, **kwargs):
        form = self.get_form()
        instance = self.get_object()


def presave_edit_form(empty_allowed_field=None):
    def decorator(view_method):
        @wraps(view_method)
        def wrapper(self, form: BaseModelForm, *args, **kwargs):
            instance = form.save(commit=False)
            for field, value in form.cleaned_data.items():  # Use .items()
                if value == "":
                    if empty_allowed_field and field in empty_allowed_field:
                        continue
                    elif hasattr(instance, field):
                        setattr(instance, field, getattr(self.get_object(), field))
            instance.save()
            return view_method(self, form, *args, **kwargs)

        return wrapper

    return decorator


def update_session(session_name: str, query_name: str, delete_key: str = "delete"):
    """
    Decorator to update a session by adding or removing elements based on client input.
    
    This decorator is designed to work with AJAX requests, where the client sends data
    indicating whether to add or remove an element from the session. The presence of the
    specified `delete_key` parameter in the request data determines the action.

    Params:
    session_name (str): The name of the session to update.
    query_name (str): The key in the request data containing the element to work with.
    delete_key (str, optional): The parameter used to decide if the received data should
        be added or deleted. Default is "delete".

    Usage:
    - Make sure the AJAX request data contains the `query_name` key for the element.
    - To add an element, send the data without the `delete_key` parameter.
    - To remove an element, send the data with the `delete_key` parameter present.
    - The decorator automatically handles updating the session data accordingly.

    Example:
    @update_session(session_name="fav_artists", query_name="artist_info")
    def post(self, request, *args, **kwargs):
        # Your view logic here
        pass
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, *args, **kwargs):
            request = self.request
            if request.method == "POST":
                if session_name in request.session:
                    current_elements = request.session[session_name]
                    input_element = request.POST[query_name]
                    if delete_key not in request.POST:
                        if input_element not in current_elements:
                            current_elements.append(input_element)
                    else:
                        if input_element in current_elements:
                            current_elements.remove(input_element)
                    if request.session[session_name].__len__() == 0:
                        del request.session[session_name]
                    else:
                        request.session[session_name] = current_elements
                    request.session.modified = True
                else:
                    request.session[session_name] = [request.POST[query_name]]
                    request.session.modified = True
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def rate_album(view_method):
    def decorator(self, *args, **kwargs):
        clean_data = rate_req_cleaner(self.request.POST)
        album = get_object_or_404(Album, pk=clean_data["album_id"])
        user = get_object_or_404(MetalHead, pk=clean_data["user_id"])
        if self.request.user.id == clean_data["user_id"]:
            album_id_str = str(clean_data["album_id"])
            if album_id_str not in user.votes.keys() or not user.votes:
                messages.success(self.request, "Thanks for rating this album. Keep rocking on !")
                new = True               
            else:
                old_rate = get_old_vote(user=user, album_id=clean_data["album_id"])
                new = False
                update_album_rating(album=album, rating=old_rate, add=False, new=new)
                messages.success(self.request, "Your rate was chenged successfully.")
            user.votes[album_id_str] = clean_data["rate"]
            update_album_rating(album=album, rating=clean_data["rate"], new=new)
            user.save()
        return view_method(self, *args, **kwargs)
    return decorator
