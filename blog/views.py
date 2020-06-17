from nis import cat

from django.shortcuts import get_object_or_404
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse

from blog.forms import CommentForm
from blog.models import Post, Category
from taggit.models import Tag


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        title = "Barrei.ro - El blog de Carlos Barreiro García"
        description = 'Artículos de opinión de Carlos Barreiro García'
        url = getattr(settings, 'HOSTNAME', "")
        context['title'] = title
        context['description'] = description
        context['url'] = url
        return context


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    template_name = 'blog/post_detail.html'
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


class CategoryPostList(generic.ListView):
    paginate_by = 10
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category__in=category.get_self_and_children_ids())

    def get_context_data(self, **kwargs):
        context = super(CategoryPostList, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        title = category.name + " - Barrei.ro"
        description = 'Entradas del blog sobre el tema de ' + category.name
        url = getattr(settings, 'HOSTNAME', "") + reverse("blog:category", kwargs={"slug": str(category.slug)})
        context['list_mode'] = 'category'
        context['category'] = category
        context['title'] = title
        context['description'] = description
        context['url'] = url
        return context


class TagPostList(generic.ListView):
    paginate_by = 10
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(tags__slug__in=[self.kwargs['slug']])

    def get_context_data(self, **kwargs):
        context = super(TagPostList, self).get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        title = "Etiqueta " + tag.name + " - Barrei.ro"
        description = 'Entradas del blog relativas a ' + tag.name
        url = getattr(settings, 'HOSTNAME', "") + reverse("blog:tag", kwargs={"slug": str(tag.slug)})
        context['list_mode'] = 'tag'
        context['tag'] = tag
        context['title'] = title
        context['description'] = description
        context['url'] = url
        return context
