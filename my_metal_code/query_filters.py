from django.db.models.query import QuerySet
from typing import Union
from django.db.models import Q
from app_management.models import Album, Artist, Member

filter_dict = {
    "most-rated":"-rating",
    "alphabet-order": "-name",
    "new-order": "-added_date",
    "slug-order": "-slug",
    "birth-date": "birth_date"
}

class QueryManager:

    def __init__(self, query_set: QuerySet, context: dict, model: Union[Album, Artist]) -> None:
        self.row_query = query_set
        self.context = context
        self.model = model

    def key_search(self) -> bool:
        if "search-query" in self.row_query:
            return True
        else:
            return False
        
    def make_q_search(self):
        key = self.row_query["search-query"]
        if isinstance(self.model(), Artist):
            result = self.model.objects.filter(Q(name__icontains=key))
            return {"key_search":result}
        elif isinstance(self.model(), Member):
            result = self.model.objects.filter(
                Q(slug__icontains=key)|
                Q(active_on__name__icontains=key)|
                Q(former_on__name__icontains=key)
            )
            return {"key_search":result}
        else:
            result = self.model.objects.filter(
                Q(name__icontains=key)|
                Q(artist__name__icontains=key)
            )
            return {"key_search":result}

    def update_context(self):
        if self.key_search():
            self.context.update(self.make_q_search())
        else:
            keys = [filter_dict[key] for key in self.row_query ]
            all_albums = self.model.objects.all().order_by(*keys)
            self.context.update({"key_search":all_albums})
            

    