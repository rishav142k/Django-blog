from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

posts = Post.objects.all()

def home(request) : 
    context = {
        "posts" : posts,
        "title" : "Home",
    }
    return render(request, "blog/home.html", context)

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name= 'posts'

    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name= 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name= "blog/post_detail.html"
    context_object_name= 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#LoginRequiredMixin: analogous to decorator @loginrequired we used for function-based view
#UserPassesTestMixin : checks if updates are done by the same user or not.

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author : 
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
    model = Post
    template_name= 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author : 
            return True
        return False    
    
    





def about(request) : 
    return render(request, "blog/about.html")
