from django.shortcuts import get_object_or_404
from django.views import generic
from django.shortcuts import render, get_object_or_404

from blog.forms import CommentForm
from blog.models import Post


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/index.html'


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


