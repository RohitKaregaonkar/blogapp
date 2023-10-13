from django.shortcuts import render
from app.models import Post

# Create your views here.
def post_page(request, slug):
    post = Post.objects.get(slug= slug)
    print(post)
    context = {"post": post}
    print('work')
    return render(request, "app/post.html", context)