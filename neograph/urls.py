from django.urls import path
from neograph.views import SearchMitre
from neograph.viewsets import SearchByKeywords

app_name = 'neograph'

urlpatterns = [
    path(r'search_mitre/', SearchMitre.as_view(), name='search_mitre'),
    path(r'search/by_keywords/<str:keywords>/',SearchByKeywords.as_view(), name='search-by-keywords'), 

]


