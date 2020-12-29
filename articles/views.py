from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Category
from .forms import CommentForm, SearchForm
from django.views.generic import ListView, DetailView
from django.db.models import Q


class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name = 'articles'
    paginate_by = 6
    template_name = 'articles/article_list.html'


# def article_category(request, category_slug=None):
#   category = None
#  categories = Category.objects.all()
# articles = Article.objects.filter(status='published')
# if category_slug:
#   category = get_object_or_404(Category, slug=category_slug)
#  articles = articles.filter(category=category)

# template = 'articles/article_detail.html'
# context = {'articles': articles,
#          'category': category,
#         'categories': categories}

# return render(request, template, context)
# def article_list(request, category_slug=None):
#   category = None
#  categories = Category.objects.all()
# articles = Article.objects.filter(status='published')
# if category_slug:
#   category = get_object_or_404(Category, slug=category_slug)
#  articles = articles.filter(category=category)
# page = request.GET.get('page', 1)
# paginator = Paginator(articles, 6)
# try:
#   pages = paginator.page(page)
# except PageNotAnInteger:
#    pages = paginator.page(1)
# except EmptyPage:
#   pages = paginator.page(paginator.num_pages)
# template = 'articles/article_list.html'
# context = {'articles': articles,
#          'category': category,
#         'categories': categories,
#        'pages': pages}
# return render(request, template, context)


def article_detail(request, year, month, day, article, category_slug=None):
    category = None
    categories = Category.objects.all()
    articles = Article.objects.filter(status='published')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=category)

    article = get_object_or_404(Article, slug=article, status='published',
                                publish__year=year, publish__month=month, publish__day=day)
    comments = article.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()

    else:
        comment_form = CommentForm()

    recent_articles = Article.published.order_by('-publish')[:5]

    return render(request, 'articles/article_detail.html', {'article': article,
                                                            'comments': comments,
                                                            'new_comment': new_comment,
                                                            'comment_form': comment_form,
                                                            'recent_articles': recent_articles,
                                                            'category': category,
                                                            'categories': categories,
                                                            'articles': articles
                                                            })


def article_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)
    return render(request, 'articles/article_list_by_category.html', {'articles': articles,
                                                                      'category': category})


#def article_search(request):
 #   form = SearchForm()
  #  query = None
   # results = []
    #if 'query' in request.GET:
     #   form = SearchForm(request.GET)
      #  if form.is_valid():
       #     query = request.GET.get('q')
        #    results = Article.objects.filter(Q(title__icontains=request.GET['query']) |
         #                                    Q(body__icontains=request.GET['query']))
    #return render(request, 'articles/search.html', {'form': form, 'query': query, 'results': results})

class SearchResultView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Article.objects.filter( Q(title__icontains=query) | Q(body__icontains=query))

