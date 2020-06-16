from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .models import UserProfileInfo, Blog, Post, Comment
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from blog.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.models import User
from django.urls import reverse
from .decorators import check_recaptcha
from django.contrib import messages
import datetime

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {"posts": posts})

def user(request, str):
    us = get_object_or_404(User, username=str)
    try:
        user = UserProfileInfo.objects.get(user=us.id)
        return render(request, 'blog/author.html', {"user": user})
    except UserProfileInfo.DoesNotExist:
        return HttpResponseNotFound("<h2>Author not found</h2>")

@login_required(login_url='/log_in')
def index(request):
    user = request.user
    return render(request, 'blog/index.html', {"user": user})

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")

@check_recaptcha
def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid() and request.recaptcha_is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'photo' in request.FILES:
                print('found it')
                profile.photo = request.FILES['photo']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'blog/sign_up.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'blog/log_in.html')

@login_required(login_url='/log_in')
def blog(request):
    User = request.user
    blogs = Blog.objects.filter(author=User)
    return render(request, "blog/new_blog.html", {"blogs": blogs})

@login_required
def create_blog(request):
    if request.method == "POST":
        blog = Blog()
        blog.title = request.POST.get('title')
        blog.category = request.POST.get('category')
        blog.date = datetime.datetime.now()
        blog.author = request.user
        blog.save()
        HttpResponse("Your blog is done.")
        return HttpResponseRedirect(reverse('blog'))
    else:
        return render(request, 'blog/create_new_blog.html')

def blog_content(request, pk):
    user = request.user
    blog = get_object_or_404(Blog, pk=pk)
    posts = Post.objects.filter(blog=blog)
    author = blog.author
    return render(request, 'blog/blog_content.html', {'blog': blog, 'posts': posts, 'user': user, 'author': author })

@login_required(login_url='/log_in')
def create_post(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        post = Post()
        post.blog = Blog.objects.get(id=blog.id)
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        post.text = request.POST.get('text')
        post.password = request.POST.get('password')
        post.date = datetime.datetime.now()
        post.author = request.user
        post.file = request.FILES.get('file')
        post.save()
        HttpResponse("Your post is done.")
        return HttpResponseRedirect(reverse('blog_content', args=[blog.id]))
    else:
        return render(request, 'blog/create_new_post.html', {'blog': blog})

@login_required(login_url='/log_in')
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        blog = post.blog
        return HttpResponseRedirect(reverse('blog_content', args=[blog.id]))
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")

@login_required(login_url='/log_in')
def delete_blog(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        return HttpResponseRedirect(reverse('blog'))
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Blog not found</h2>")

def post_password(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.password:
        return HttpResponseRedirect(reverse('get_password', args=[post.id]))
    else:
        return HttpResponseRedirect(reverse('post_content', args=[post.id]))

def get_password(request, pk):
    try:
        correct = True
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            password = request.POST.get('password')
            if password == post.password:
                return HttpResponseRedirect(reverse('post_content', args=[post.id]))
            else:
                correct = False
        return render(request, 'blog/get_password.html', {'post': post, 'correct': correct })
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")

def post_content(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    post_cont = Post.objects.get(id=post.id)
    blog = post.blog
    comments = Comment.objects.filter(post=post)
    return render(request, 'blog/post_content.html', {'post': post, 'post_cont': post_cont, 'comments': comments, 'blog':blog, 'user': user })

@login_required(login_url='/log_in')
@check_recaptcha
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        comment = Comment()
        comment.post = Post.objects.get(id=post.id)
        comment.author = request.user
        comment.text = request.POST.get('text')
        comment.date = datetime.datetime.now()
        if request.recaptcha_is_valid:
            comment.save()
            messages.success(request, 'New comment added with success!')
            return HttpResponseRedirect(reverse('post_content', args=[post.id]))
    return render(request, 'blog/post_content.html', {'post': post, 'comment': comment })

@login_required(login_url='/log_in')
def edite_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            post.title = request.POST.get('title')
            post.description = request.POST.get('description')
            post.text = request.POST.get('text')
            if 'file' in request.FILES:
                post.file = request.FILES.get('file')
            post.save()
            return HttpResponseRedirect(reverse('blog_content', args=[post.blog.id]))
        else:
            return render(request, 'blog/edite_post.html', {'post': post })
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")

@login_required(login_url='/log_in')
def edite_password(request, pk):
    correct = True
    try:
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == post.password:
                post.password = password2
                post.save()
                return HttpResponseRedirect(reverse('post_content', args=[post.id]))
            else:
                correct = False
        return render(request, 'blog/edite_password.html', {'post': post, 'correct': correct })
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")

@login_required(login_url='/log_in')
def edite_blog(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        if request.method == "POST":
            blog.title = request.POST.get('title')
            blog.category = request.POST.get('category')
            blog.save()
            return HttpResponseRedirect(reverse('blog'))
        else:
            return render(request, 'blog/edite_blog.html', {'blog': blog })
    except Blog.DoesNotExist:
        return HttpResponseNotFound("<h2>Blog not found</h2>")

def search_results(request, str):
        search = str
        if search == 'all':
            posts =  Post.objects.all()
        else:
            posts = Post.objects.filter(title=str)
        return render(request, 'blog/search.html', {'posts': posts, 'search': search})

def search_form(request):
    if request.method == "POST":
        title_s = request.POST.get('title')
        author_s = request.POST.get('author')
        date_s = request.POST.get('date')
        if not title_s:
            title_s = ' '
        if not author_s:
            author_s = ' '
        if not date_s:
            date_s = datetime.date(1000, 1, 1)
        return HttpResponseRedirect(reverse('search_ss', args=[title_s, author_s, date_s]))

def search_ss(request, title, author, date):
    date_ = datetime.datetime(1000, 1, 1)
    search = title
    search_date = datetime.datetime.strptime(date, '%Y-%m-%d')

    if author == ' ':
        posts = Post.objects.all()
    else:
        try:
            user = User.objects.get(username=author)
            posts = Post.objects.filter(author=user.id)
        except User.DoesNotExist:
            posts = Post.objects.all()

    if search == ' ':
        pass
    else:
        posts = posts.filter(title=search)

    if search_date == date_:
       pass
    else:
        posts = posts.filter(date__day=search_date.day, date__year=search_date.year, date__month=search_date.month )

    if (author == ' ' and search == ' ' and search_date == date_):
        posts = Post.objects.all()

    return render(request, 'blog/search.html', {'posts': posts, 'search': search})

def search_s(request):
    if request.method == "POST":
        search = request.POST.get('q')
        if not search:
            search = 'all'
        return HttpResponseRedirect(reverse('search_results', args=[search]))














