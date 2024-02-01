from django.urls import path
from .views import *

urlpatterns = [
        path("upload/", PostCreateView.as_view(), name="upload_post"),
        path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
        path("", home, name="home_page"),
        # path("view/<link_uuid>/<access_link>", view_posts, name="view_posts")
]