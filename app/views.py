from django.shortcuts import render, redirect
from app.models import Post, Comments
from app.forms import CommentForm
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug= slug)
    comments = Comments.objects.filter(post= post, parent= None)
    form = CommentForm()
    
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            postid = request.POST.get('post_id')
            post = Post.objects.get(id= postid)

            if request.POST.get('parent'):
                parent_id = request.POST.get('parent')
                parent = Comments.objects.get(id= parent_id)
                comment.post = post
                comment.parent = parent
                comment.save()
            else:
                comment.post = post
                comment.save()
                
            return redirect(reverse('post_page', kwargs={'slug': post.slug}))
    
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, "app/post.html", context)

