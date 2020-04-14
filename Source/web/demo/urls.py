from django.conf.urls import url
import modl.China_world_data
from view import index, search, map, data_st, answering

urlpatterns = [
    url(r'^$', index.search),
    url(r'^data_st', data_st.data_st),
    url(r'^search_relation', search.search_relation),
    url(r'^qa', answering.answering),
    url(r'^map_china', map.china_map),
    url(r'^map_world', map.world_map),
    url(r'^search_st', search.search_st),
    url(r'^search', index.search),
    url(r'^ajax_china_data', map.ajax_china),
    url(r'^ajax_world_data', map.ajax_world)
]
