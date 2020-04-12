from django.conf.urls import url
# from . import tagging_data_view,tagging_data_writefile_view
# from . import _404_view, overview_view
# from . import relation_view
# from . import tagging
# from . import question_answering
import modl.China_world_data
from view import index, nlp, search, map, data_st, answering

urlpatterns = [
    url(r'^$', search.search_relation),
    url(r'^data_st', data_st.data_st),
    url(r'^search_relation', search.search_relation),
    url(r'^qa', answering.answering),
    url(r'^map_china', map.china_map),
    url(r'^map_world', map.world_map),
    url(r'^nlpltp', nlp.nlp_fc),
    url(r'^search_st', search.search_st),
    url(r'^search', index.search),


    
]
