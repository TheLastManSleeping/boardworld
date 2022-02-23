from allauth.account.views import PasswordChangeView
from django.conf.urls import url
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from . import views
from .models import Profile

urlpatterns = [
    path("", views.GamesView.as_view(), name ='game'),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<slug:slug>/", views.GamesDetailView.as_view(), name="game_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("publisher/<str:slug>/", views.PublisherView.as_view(), name="publisher_detail"),
    # url(r'^accounts/profile/$', ProfilePage.as_view(), name="profile"),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("accounts/profile/", views.ProfileView.as_view(), name='profile'),
]
