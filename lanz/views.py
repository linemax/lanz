from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import Send, CommentF
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = Send(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read" \
                      f"{post.title}"
            message = f" Read{post.title} at {post_url}\n\n" \
                      f" {cd['name']} s' comments: {cd['comments']}"
            send_mail(subject, message, 'roblineyegon@gmail.com', [cd['to']])
            sent = True
    else:
        form = Send()
    return render(request, 'lanz/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})


def post_list(request):
    object_list = Post.published.all()
    pager = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = pager.page(page)
    except PageNotAnInteger:
        posts = pager.page(1)
    except EmptyPage:
        posts = pager.page(pager.num_pages)
    return render(request, 'lanz/post/list.html',
                  {'posts': posts,
                   "page": page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = None
    if request.method == 'POST':
        comment_form = CommentF(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentF()
    return render(request, 'lanz/post/detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'lanz/post/list.html'
    paginate_by = 3


class Url(ListView):
    template_name = 'lanz/post/list.html'
    queryset = Post.published.all()
    context_object_name = 'posts'
