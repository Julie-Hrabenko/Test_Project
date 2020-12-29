from django.urls import path

from . views import ArticleListView, article_detail, SearchResultView, article_category


urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('search/', SearchResultView.as_view(), name='search'),
    path('<slug:slug>/', article_category, name='article_list_by_category'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>/', article_detail, name='article_detail')
]
