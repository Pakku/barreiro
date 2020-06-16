from nis import cat

from django.shortcuts import get_object_or_404
from django.views import generic
from django.shortcuts import render, get_object_or_404

from blog.forms import CommentForm
from blog.models import Post, Category
from taggit.models import Tag


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/index.html'
    paginate_by = 10


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
        context['list_mode'] = 'category'
        context['category'] = category
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
        context['list_mode'] = 'tag'
        context['tag'] = tag
        return context
