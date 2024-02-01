from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

class PostCreateView(LoginRequiredMixin, CreateView):
        model = Post
        template_name = 'mainapp/post_upload.html'
        fields = ['context', 'post']
        
        def form_valid(self,form):
                form.instance.author = self.request.user
                return super().form_valid(form)
        
class PostDetailView(LoginRequiredMixin, DetailView):
        model = Post

class PostDetailViewUser(DetailView):
        model = Post
        
@login_required
def home(request):
        posts = Post.objects.filter(author=request.user).order_by("-date_posted")
        the_author = request.user.first_name
        the_dp = request.user.profile.image.url
        return render(request, "mainapp/home.html", {"posts":posts, "the_author":the_author,"the_dp":the_dp})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
        model = Post
        fields = ['context', 'post']
        
        def form_valid(self,form):
                form.instance.author = self.request.user
                return super().form_valid(form)
        
        def test_func(self):
                post = self.get_object()
                return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
        model = Post
        success_url = '/'
        
        def test_func(self):
                post = self.get_object()
                return self.request.user == post.author
        
        