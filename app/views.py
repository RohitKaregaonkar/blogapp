from django.shortcuts import render, redirect
from app.models import Post, Comments, Tag, Profile
from app.forms import CommentForm, SubscribeForm
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def index(request):
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    new_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_posts = Post.objects.all().filter(featured= True)[0]
    subscribe_form = SubscribeForm()
    subscribe_success = None
    
    if request.POST:
        subscribe_form_result = SubscribeForm(request.POST)
        if subscribe_form_result.is_valid():
            subscribe_form_result.save()
            subscribe_success = "Subscribed Successfully"  
        return redirect('index')      
    
    context = {'top_posts': top_posts, 'new_posts': new_posts, 'subscribe_form': subscribe_form, 'featured_posts': featured_posts,'subscribe_success': subscribe_success}
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



def tag_page(request, slug):
    tag = Tag.objects.get(slug= slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')
    featured_posts = Post.objects.filter(tags__in=[tag.id]).filter(featured= True).order_by('-last_updated')
    tags = Tag.objects.all()
    context = {'tag': tag, 'top_posts': top_posts, 'recent_posts': recent_posts, 'featured_posts': featured_posts, 'tags': tags}
    return render(request, 'app/tag.html', context)


def author_page(request, slug):
    profile = Profile.objects.get(slug= slug)
    top_posts = Post.objects.filter(tags__in=[profile.id]).order_by('-view_count')
    recent_posts = Post.objects.filter(tags__in=[profile.id]).order_by('-last_updated')
    featured_posts = Post.objects.filter(tags__in=[profile.id]).filter(featured= True).order_by('-last_updated')
    authors = Profile.objects.all()
    context = {'profile': profile, 'top_posts': top_posts, 'recent_posts': recent_posts, 'featured_posts': featured_posts, 'authors': authors}
    return render(request, 'app/author.html', context)