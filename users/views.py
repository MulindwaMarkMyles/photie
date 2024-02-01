from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SharePostsForm, AccessLinkLoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, DeleteView

import uuid
from . import utilities
from mainapp.models import Post
from django.contrib.auth.models import User
from .models import AccessLink

def register(request):
        if request.method == "POST":
                form = UserRegisterForm(request.POST)
                if form.is_valid():
                        form.save()
                        username = form.cleaned_data.get("username")
                        messages.success(request, f"Account created for {username}!")
                        return redirect("login")
        else:
                form = UserRegisterForm()
        return render(request, "users/register.html", {"form":form})
        
def logout_view(request):
        logout(request)
        messages.success(request, "Successfully logged out!")
        return redirect("login")

@login_required
def profile(request):
        if request.method == "POST":
                u_form = UserUpdateForm(request.POST, instance=request.user)
                p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
                        u_form.save()
                        p_form.save()
                        messages.success(request, "Successfully updated account!")
                        return redirect("profile")
        else:
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
                
        return render(request, "users/profile.html", {"u_form":u_form, "p_form":p_form})

@login_required
def share_posts(request):
        if request.method == "POST":
                form = SharePostsForm(request.POST)
                if form.is_valid():
                        form.save()
                        utilities.send_message(request.user.first_name, request.user.last_name, request.POST.get("email"), request.POST.get("access_token"), request.POST.get("name"))
                        messages.success(request, "Successfully sent the invite email!")
                        return redirect("profile")
        else:
                form = SharePostsForm(initial={"access_token":uuid.uuid4(),"username":request.user.username})
        return render(request, "users/share_posts.html",{"form":form})

def view_posts(request, username, token):
        try:
                uuid_obj = uuid.UUID(str(token))
        except ValueError:
                return redirect("login_using_access_token")
        else:
                user = User.objects.filter(username=username).first()
                posts = Post.objects.filter(author=user).order_by("-date_posted")
                the_author = user.first_name
                the_dp = None
                return render(request, "mainapp/home.html", {"posts":posts, "the_author":the_author,"the_dp":the_dp})

def login_view_access_tokens(request):
        if request.method == "POST":
                form = AccessLinkLoginForm(request.POST)
                if form.is_valid():
                        email = form.cleaned_data.get("email")
                        access_token = form.cleaned_data.get("access_token")
                        if not AccessLink.objects.filter(access_token=access_token, email=email).exists():
                                messages.error(request,"Invalid entries please check the email and access token.")
                        else:
                                username = AccessLink.objects.filter(email=email).first().username
                                return redirect("view_posts", username=username, token=access_token)
        else:
                form = AccessLinkLoginForm(initial={"access_token":"Example: fa14ce2d-d940-5a79-8e1c-ea087925176b","email":"Example: email@email.com"})
        return render(request, "users/login_access.html", {"form": form})

@login_required
def view_followers(request):
        followers = AccessLink.objects.filter(username=request.user.username).order_by("-created_at")
        if followers.count() == 0:
                messages.info(request, "You have no followers yet.")
                return redirect("profile")
        return render(request, "users/view_followers.html",{"followers":followers})

class FollowerInfo(LoginRequiredMixin, UserPassesTestMixin, DetailView):
        model = AccessLink
        
        def form_valid(self,form):
                form.instance.author = self.request.user
                return super().form_valid(form)
        
        def test_func(self):
                access_link = self.get_object()
                return self.request.user.username == access_link.username
        
@login_required
def follower_info(request, pk):
        access_link = AccessLink.objects.filter(pk=pk).first()
        return render(request, "users/follower_info.html", {"access_link": access_link})

class AccessLinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
        model = AccessLink
        success_url = '/view/followers'
        
        def test_func(self):
                access_link = self.get_object()
                return self.request.user.username == access_link.username