from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView

#just  a variable
_user = ""

class PostCreateView(LoginRequiredMixin, CreateView):
        model = Post
        template_name = 'mainapp/image_upload.html'
        fields = ['context', 'post']
        
        def form_valid(self,form):
                form.instance.author = self.request.user
                return super().form_valid(form)
        
class PostDetailView(LoginRequiredMixin, DetailView):
        model = Post
        
@login_required
def home(request):
        posts = Post.objects.filter(author=request.user).order_by("-date_posted")
        the_author = request.user.first_name
        the_dp = request.user.profile.image.url
        return render(request, "mainapp/home.html", {"posts":posts, "the_author":the_author,"the_dp":the_dp})


        
# def view_posts(request, link_uuid, user):
#         access_link = get_object_or_404(AccessLink, link_uuid=link_uuid, posts_owner=user)
#         posts = Post.objects.filter(author=request.user).order_by("-date_posted")
#         the_author = request.user.first_name
#         the_dp = None
#         return render(request, "mainapp/home.html", {"posts":posts, "the_author":the_author,"the_dp":the_dp})
        
        