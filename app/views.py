from django.shortcuts import render, redirect, get_object_or_404
from app.models import Post, Comments, Tag, Profile, WebsiteMeta
from app.forms import CommentForm, SubscribeForm, NewUserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login


# Create your views here.
def index(request):
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    new_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_posts = Post.objects.all().filter(featured= True)
    subscribe_form = SubscribeForm()
    subscribe_success = None
    website_info = None
    
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_posts:
        featured_posts = featured_posts[0]
    
    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            subscribe_success = "Subscribed Successfully"  
            subscribe_form = SubscribeForm()
          
    
    context = {'top_posts': top_posts, 'website_info':website_info, 'new_posts': new_posts, 
               'subscribe_form': subscribe_form, 'featured_posts': featured_posts,'subscribe_success': subscribe_success}
    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug= slug)
    comments = Comments.objects.filter(post= post, parent= None)
    form = CommentForm()
    
    # Bookmark logic
    bookmarked = False
    if post.bookmarks.filter(id = request.user.id).exists():
        bookmarked = True
    is_bookmarked = bookmarked
    
    # Liked logic
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes()
    is_liked = liked
    
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
    
    
    #sidebar
    recent_posts = Post.objects.exclude(id = post.id).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')
    tags = Tag.objects.all()
    related_posts = Post.objects.exclude(id = post.id).filter(author=post.author)[0:3]
    
    context = {'post': post, 'form': form, 'is_bookmarked':is_bookmarked, 'comments': comments,
               'is_liked': is_liked, 'number_of_likes': number_of_likes,
               'recent_posts': recent_posts, 'top_authors': top_authors,
               'related_posts': related_posts, 'tags': tags
               }
    
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


def search_post(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    context = {'posts': posts, 'search_query': search_query}
    return render(request, 'app/search.html', context)

def about_page(request):
    website_info = None
    
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
        
    context = {'website_info': website_info}
    return render(request, 'app/about.html', context)


def register_user(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        
    context = {'form': form}
    return render(request, 'registration/registration.html', context)


def bookmark_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    #get_object_or_404 is a function which does a get call on any given model that you pass.

    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))


def all_bookmarked_posts(request):
    all_bookmarked_posts = Post.objects.filter(bookmarks=request.user)
    context={'all_bookmarked_posts':all_bookmarked_posts}
    return render(request, 'app/all_bookmarked_posts.html', context)

def all_posts(request):
    all_posts = Post.objects.all()
    context={'all_posts':all_posts}
    return render(request, 'app/all_posts.html', context)

def all_liked_posts(request):
    all_liked_posts = Post.objects.filter(likes=request.user)
    context={'all_liked_posts':all_liked_posts}
    return render(request, 'app/all_liked_posts.html', context)