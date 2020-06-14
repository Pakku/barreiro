from django.contrib.auth.models import User
from django.db import models
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    content = models.TextField()
    image = FilerImageField(related_name='blog_images', null=True, on_delete=models.SET_NULL, blank=True)
    summary = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, blank=True, related_name='blog_posts')
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:post_detail", kwargs={"slug": str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural='categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('blog:category', kwargs={"slug": str(self.slug)})

    def get_self_and_children_ids(self):
        ids = [self.id]
        for category in self.children.all():
            ids = ids + category.get_self_and_children_ids()
        return ids;
