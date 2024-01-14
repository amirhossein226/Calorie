from django.shortcuts import render,get_object_or_404
from django.http import Http404
from .models import Post, Comment
from django.core.paginator import \
        Paginator,\
        EmptyPage,\
        PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag



# Create your views here.


@require_POST
def post_comment(request, post_id):
    
    post = get_object_or_404(Post, id = post_id, \
            status = Post.Status.PUBLISHED)
    comment = None

    form =  CommentForm(request.POST)
    if form.is_valid:
        comment = form.save(commit = False)
        comment.post = post
        comment.save()
    return render(request, "blog/post/comment.html",
                  {"form":form,
                   "post":post,
                   "comment":comment})



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False


    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri\
                    (post.get_absolute_url())
            subject = f"{cd['name']} recommands you \
                    read {post.title}"
            message = f"Read {'post.title'} at {post_url}\n\n\n"\
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, "amirsardari226@gmail.com", [f"cd['to']"])

            sent = True
                    
    else:
        form = EmailPostForm()

    return render(request, "blog/post/share.html",{
        "post":post,
        "form":form,
        "sent":sent
        })

def post_list(request, tag_slug = None):
    post_lists = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_lists = post_lists.filter(tags__in=[tag])

    paginator = Paginator(post_lists, 3)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  "blog/post/list.html",
                  {"posts":posts,
                   "tag":tag})

def post_detail(request,year,month,day,post):
    
    post = get_object_or_404(Post, 
                             status=Post.Status.\
                                     PUBLISHED,
                             slug=post,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day,
                             )
    all_comments = post.comments.filter(active=True)
    paginator = Paginator(all_comments, 3)
    page_number = request.GET.get("page", 1)

    comments = paginator.page(page_number)

    form = CommentForm()

    return render(request, "blog/post/detail.html",\
            {
                "post":post,
                "comments":comments,
                "form":form,
             })



