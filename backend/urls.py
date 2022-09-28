from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from backend.views import views

urlPatterns = [
    path('article/<str:articleId>/', views.article.as_view()),
    path("login/<str:userId>/", views.login_user),
]

urlpatterns = format_suffix_patterns(urlPatterns)