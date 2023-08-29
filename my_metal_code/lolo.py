# from my_metal_code.db_helper import fav_req_cleaner
# from db_helper import fav_req_cleaner
from ...imdb.my_metal_code.db_helper import fav_req_cleaner
mydict = {'csrfmiddlewaretoken': ['t2NjWk5VLctaW2AkxnlktnTpyfbyIi2piMGjuQTO6BEJLlXhaweIALrlHYegpBwV'], 'rate': ['1'], 'album_id': ['8'], 'user_id': ['2']}

print(mydict)
newdict = fav_req_cleaner(mydict)
print(newdict)