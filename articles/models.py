from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model


class PublishedManager(models.Manager):
    def get_query(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    objects = models.Manager()
    slug = models.SlugField(max_length=150, unique=True)  # default=uuid.uuid4

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article_list_by_category', args=[self.slug])


class Article(models.Model):
    category = models.ForeignKey('Category', null=True, verbose_name='category', on_delete=models.CASCADE)
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=255, null=False, default='test2')
    slug = models.SlugField(max_length=64, blank=True, unique_for_date='publish')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='articles', null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    body = models.TextField(default='test2')
    image = models.ImageField(upload_to='article_image', blank=True)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments', null=True)
    name = models.CharField(max_length=80, default='')
    email = models.EmailField()
    body = models.TextField(blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on', ]

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
