from django.shortcuts import render, Http404, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Post, Comment
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.

def blog(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'blog.html', {'posts':posts})

class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ['-date_stamp']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feature"] = Post.objects.filter(featured=True)[:6] 
        return context
    
    paginate_by = 6



class UserPostListView(ListView):
    model = Post
    template_name = 'user_post.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'objects': Post.objects.all().order_by('-date_stamp')[:5] 
        })  
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_stamp')

class CategoryPostListView(ListView):
    model = Post
    template_name = 'category_post.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'objects': Post.objects.all().order_by('-date_stamp')[:5] 
        })  
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Post.objects.filter(category=category).order_by('-date_stamp')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image', 'body', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'body', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user.post_set.get(slug=self.kwargs.get('slug')),
        })  
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        place = self.get_object()
        if self.request.user == place.author:
            return True
        return False

# class PostDetailView(DetailView):
#     model = Post
#     query_pk_and_slug = True

def single(request, pk, slug):
    post = Post.objects.get(slug=slug)
    categories = Category.objects.get(post=post)
    feature = Post.objects.filter(featured=True)[:4]
    #comments
    comments = post.comments.all()
    if request.POST:
        writer = request.POST['name']
        email = request.POST['email']
        website = request.POST['website']
        message = request.POST['message']

        comment = Comment.objects.create(
            post = post,
            writer=writer,
            email=email,
            website=website,
            message=message,
            date_stamp=datetime.now()
        )
        comment.save()
    context = {
        'object':post, 
        'categories':categories,
        'comments':comments,
        'feature':feature
    }
    return render(request, 'blog/post_detail.html', context)
    

def search(request):
    query = request.GET['query']
    posts = Post.objects.filter(title__icontains=query)|Post.objects.filter(body__icontains=query)
    return render(request, 'search.html', {'posts':posts, 'query':query})

