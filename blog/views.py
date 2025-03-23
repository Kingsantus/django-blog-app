from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.http import Http404

# Create your views here.
def post_list(request):
    # get all post with published true
    post_list = Post.published.all()
    # paginator to return first 5
    paginator = Paginator(post_list, 5)
    # page number to be returned starting from 1
    page_number = request.GET.get('page', 1)
    # try and except if the following
    try:
        # page number is within range
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # user added string or etc other than integer to page use the first page
        posts = paginator.page(1)
    except EmptyPage:
        # user add more number than available use the last page
        posts = paginator.page(paginator.num_pages)

    # return the value of the post in a html
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    # get ot throw error
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No Post found.')
    
    # pass post into html file and render it there
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )