from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from .form.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
# from django.http import Http404

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# Create your views here.
# def post_list(request):
#     # get all post with published true
#     post_list = Post.published.all()
#     # paginator to return first 5
#     paginator = Paginator(post_list, 5)
#     # page number to be returned starting from 1
#     page_number = request.GET.get('page', 1)
#     # try and except if the following
#     try:
#         # page number is within range
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # user added string or etc other than integer to page use the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # user add more number than available use the last page
#         posts = paginator.page(paginator.num_pages)

#     # return the value of the post in a html
#     return render(
#         request,
#         'blog/post/list.html',
#         {'posts': posts}
#     )


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
    
    # list of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    # pass post into html file and render it there
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        }
    )


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f'{cd['name']} ({cd['email']})'
                f'recommends you read {post.title}'
            )
            message = (
                f'Read {post.title} at {post_url}\n\n'
                f'{cd['name']}\'s comments: {cd['comments']}'
            )
            print(subject, message)
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
                fail_silently=False,
            )
            sent = True

    else:
            form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    req = request.POST

    # A comment was posted
    form = CommentForm(data=req)

    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save comment to the database
        comment.save()

    return render(
         request,
         'blog/post/comment.html',
         {
              'post': post,
              'form': form,
              'comment': comment
         }
    )
