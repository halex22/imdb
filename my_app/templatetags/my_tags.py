from django import template

register = template.Library()


@register.filter(name="divide")
def divide(value, arg):
    try:
        return value / arg
    except (ValueError, ZeroDivisionError):
        return value
    

@register.filter(name="has_voted")
def has_voted(user_votes: dict, album_id:  int) -> bool:
    if str(album_id) in user_votes.keys():
        return True
    

@register.filter(name="get_user_rate")
def get_user_rate(user_votes: dict, album_id:  int) -> float:
    return user_votes[str(album_id)]