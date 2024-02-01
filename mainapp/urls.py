from django.urls import path
from .views import *

urlpatterns = [
        path("upload/", PostCreateView.as_view(), name="upload_post"),
        path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
        path('post/<int:pk>/user', PostDetailViewUser.as_view(template_name="mainapp/post_detail_2.html"), name="post-detail-user"),
        path("", home, name="home_page"),
        path('post/update/<int:pk>', PostUpdateView.as_view(template_name="mainapp/post_upload.html"), name="post-update"),
        path('post/delete/<int:pk>', PostDeleteView.as_view(), name="post-delete"),
]