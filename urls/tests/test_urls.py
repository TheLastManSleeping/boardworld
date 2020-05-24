from django.urls import resolve, reverse
from urls.views import GamesDetailView, AddReview, PublisherView, signup, activate, SendEmailView, SearchView


class TestUrls:

    def test_search_url(self):
        path = reverse('search')
        assert resolve(path).view_name == 'search'
        assert resolve(path).func.view_class == SearchView

    def test_game_detail_url(self):
        path = reverse('game_detail', args=['some-slug'])
        assert resolve(path).view_name == 'game_detail'
        assert resolve(path).func.view_class == GamesDetailView

    def test_add_review_url(self):
        path = reverse('add_review', kwargs={'pk': '1'})
        assert resolve(path).view_name == 'add_review'
        assert resolve(path).func.view_class == AddReview

    def test_publisher_detail_url(self):
        path = reverse('publisher_detail', args=['some-slug'])
        assert resolve(path).view_name == 'publisher_detail'
        assert resolve(path).func.view_class == PublisherView

    def test_signup_url(self):
        path = reverse('signup')
        assert resolve(path).view_name == 'signup'
        assert resolve(path).func == signup

    def test_save_item_url(self):
        path = reverse('signup')
        assert resolve(path).view_name == 'signup'
        assert resolve(path).func == signup

    def test_activate_url(self):
        path = reverse('activate', kwargs={'uidb64': 'Njc', 'token': '5gg-0cb3b3b4f111ed7029fa'})
        assert resolve(path).view_name == 'activate'
        assert resolve(path).func == activate

    def test_send_email_url(self):
        path = reverse('email')
        assert resolve(path).view_name == 'email'
        assert resolve(path).func.view_class == SendEmailView
