from allauth.account.views import PasswordChangeView
from django.conf.urls import url
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from . import views
from .models import Profile
from .views import activation_email_sent, activate, SendEmailView, ProfilePage


urlpatterns = [
    path("", views.GamesView.as_view(), name ='game'),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<slug:slug>/", views.GamesDetailView.as_view(), name="game_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("publisher/<str:slug>/", views.PublisherView.as_view(), name="publisher_detail"),
    path("accounts/signup/", views.signup, name='signup'),
    path("account_activation_sent", activation_email_sent, name='activation_email_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^send_email$', SendEmailView.as_view(), name='email'),
    url(r'^accounts/profile/$', ProfilePage.as_view(), name="profile"),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
