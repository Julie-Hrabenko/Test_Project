from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='available')


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    objects = models.Manager()
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, verbose_name='category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True, default='')
    slug = models.SlugField(max_length=64, unique=True, blank=True)
    image = models.ImageField(upload_to='product_image', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    published = PublishedManager()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name', ]
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])
