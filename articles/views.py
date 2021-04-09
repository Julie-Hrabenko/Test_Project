from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from .forms import CommentForm
from django.views.generic import ListView
from django.db.models import Q


class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name = 'articles'
    paginate_by = 6
    template_name = 'articles/article_list.html'



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


class SearchResultView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Article.objects.filter( Q(title__icontains=query) | Q(body__icontains=query))

