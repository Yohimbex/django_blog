from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    """Show only published posts"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class DraftManager(models.Manager):
    """Show only draft posts"""
    def get_queryset(self):
        return super().get_queryset().filter(status='draft')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=200)  # Назва
    slug = models.SlugField(
        max_length=200,
        unique_for_date='publish',
    )  # Відображається в адресному рядку
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Видалення всіх постів користувача, якщо видалили користувача
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # Щоб знати дату публікації
    created = models.DateTimeField(auto_now_add=True)  # Щоб знати коли було створено користувача
    updated = models.DateTimeField(auto_now=True)  # Щоб знати дату оновлення
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    tags = TaggableManager()
    objects = models.Manager
    published = PublishedManager()
    draft = DraftManager()

    class Meta:
        ordering = ('-publish', )  # Щоб найновіші пости відображались першими

    def __str__(self):
        return f'{self.title[:19]}...'

    def get_absolute_url(self):
        return reverse(
            'blog:post_details',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ])


class Comments(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
