from django.conf.urls import url
# from . import tagging_data_view,tagging_data_writefile_view
# from . import _404_view, overview_view
# from . import relation_view
# from . import tagging
# from . import question_answering
from view import index, nlp, search, map, data_st

urlpatterns = [
    url(r'^$', index.index),
    url(r'^data_st', data_st.data_st),
    # url(r'^tagging_data', tagging_data_view.showtagging_data),
    # url(r'^tagging-get', tagging_data_writefile_view.tagging_push),
    # url(r'^overview', overview_view.show_overview),
    # url(r'^404', _404_view._404_),
    # url(r'^search_entity', relation_view.search_entity),
    # url(r'^tagging', tagging.tagging),
    url(r'^search_relation', search.search_relation),
    # url(r'^qa', question_answering.question_answering),
    url(r'^map_china', map.china_map),
    url(r'^map_world', map.world_map),
    url(r'^nlpltp', nlp.nlp_fc),
    url(r'^search_st', search.search_st),
    url(r'^search', index.search),


    
]
