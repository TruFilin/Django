from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        post_rating_sum = 0
        comment_rating_sum = 0
        post_comment_rating_sum = 0
        for post in self.post_set.all():
            post_rating_sum += post.rating * 3

        for comment in self.user.comment_set.all():
            comment_rating_sum += comment.rating

        for post in self.post_set.all():
            for comment in post.comment_set.all():
                post_comment_rating_sum += comment.rating

        self.rating = post_rating_sum + comment_rating_sum + post_comment_rating_sum
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NE'
    POST_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)  # Время создания поста
    time_written = models.DateTimeField(default=timezone.now)  # Время написания поста
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    class Post(models.Model):
        ARTICLE = 'AR'
        NEWS = 'NE'
        POST_CHOICES = [
            (ARTICLE, 'Статья'),
            (NEWS, 'Новость'),
        ]

        author = models.ForeignKey(Author, on_delete=models.CASCADE)
        post_type = models.CharField(max_length=2, choices=POST_CHOICES)
        created_at = models.DateTimeField(default=timezone.now)
        categories = models.ManyToManyField(Category, through='PostCategory')
        title = models.CharField(max_length=255)
        content = models.TextField()
        rating = models.IntegerField(default=0)

        def preview(self):
            preview_length = 124
            if len(self.content) > preview_length:
                return self.content[:preview_length] + "..."
            else:
                return self.content

        def like(self):
            self.rating += 1
            self.author.update_rating()
            self.save()

        def dislike(self):
            self.rating -= 1
            self.author.update_rating()
            self.save()

        def str(self):
            return self.title

    def preview(self):
        preview_length = 124
        if len(self.content) > preview_length:
            return self.content[:preview_length] + "..."
        else:
            return self.content

    def like(self):
        self.rating += 1
        self.author.update_rating()
        self.save()

    def dislike(self):
        self.rating -= 1
        self.author.update_rating()
        self.save()

    def str(self):
        return self.title
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

    def like(self):
        self.rating += 1
        self.post.author.update_rating()
        self.save()

    def dislike(self):
        self.rating -= 1
        self.post.author.update_rating()
        self.save()