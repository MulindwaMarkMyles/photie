from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SharePostsForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import AccessLink
import uuid
from . import utilities

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
                        # utilities.send_message(request.user.first_name, request.user.last_name, request.POST.get("email"), request.POST.get("access_token"), request.POST.get("name"))
                        messages.success(request, "Successfully sent the invite email!")
                        return redirect("profile")
        else:
                form = SharePostsForm(initial={"access_token":uuid.uuid5,"username":request.user.username})
        return render(request, "users/share_posts.html",{"form":form})