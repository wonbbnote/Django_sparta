from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path("logout/", views.logout, name="logout"),
    path("user/", views.user_view, name="user-list"),
    path("user/follow/<int:id>/", views.user_follow, name="user-follow"),
]

# '~/sign-up/'이라는 url만들어줌 -> 이 url로 접근 시 views.py에 있는 sign_up_view 함수가 실행됨

