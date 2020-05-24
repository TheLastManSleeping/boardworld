import mixer as mixer
import pytest
from django.contrib.admin import AdminSite
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer

from urls.admin import CustomUserAdmin
from urls.tokens import account_activation_token
from urls.views import SearchView, activate, signup, SendEmailView


@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def anonymous_user():
    return AnonymousUser()

@pytest.fixture
def staff_user(db):
    user = mixer.blend(User, is_staff=True, password='test_pass123')
    user.profile.verified = True
    return user

@pytest.fixture
def not_staff_user(db):
    user = mixer.blend(User, is_staff=False, password='test_pass123')
    user.profile.verified = True
    return user

def middleware_anotate(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

    middleware = MessageMiddleware()
    middleware.process_request(request)
    request.session.save()



@pytest.mark.django_db
@pytest.mark.filterwarnings('ignore::Warning')
class TestView:
    def test_game_view(self, client):
        path = reverse('game')

        assert client.get(path).status_code == 200

    def test_search_view(self, request_factory):
        path = reverse('search')
        request = request_factory.get(path, {'q': 'foo'})

        view = SearchView()
        view.setup(request)
        view.object_list = view.get_queryset()
        context = view.get_context_data()

        assert context['search'] == True

    def test_activation_email_sent(self, client):
        path = reverse('activation_email_sent')

        assert client.get(path).status_code == 200

    def test_signup_view_not_authenticated_post(self, request_factory, anonymous_user):
        path = reverse('signup')
        request = request_factory.post(path, {'username': 'test_user', 'email': 'test@test.com', 'password1': 'eokdo254ihjb', 'password2': 'eokdo254ihjb'})
        request.user = anonymous_user

        view = signup(request)

        assert view.status_code == 302

        request = request_factory.post(path, {'email': 'test@test.com', 'password1': 'eokdo254ihjb', 'password2': 'eokdo254ihjb'})
        request.user = anonymous_user

        assert view.status_code == 302

    def test_signup_view_not_authenticated_get(self, request_factory, anonymous_user):
        path = reverse('signup')
        request = request_factory.get(path)
        request.user = anonymous_user

        view = signup(request)

        assert view.status_code == 200


    def test_send_email_admin_action(self, request_factory, staff_user):
        model = CustomUserAdmin(User, AdminSite())

        assert model.send_email(HttpRequest(), [staff_user]).status_code == 200


    def test_send_email_view(self, request_factory, not_staff_user, staff_user):
        path = reverse('email')
        request = request_factory.post(path, {'subject': 'test', 'message': 'test', 'users': [not_staff_user.pk]})
        request.user = staff_user
        middleware_anotate(request)
        view = SendEmailView()
        view.setup(request)

        assert view.post(request).status_code == 302

        request = request_factory.post(path, {'message': 'test', 'users': [not_staff_user.pk]})
        request.user = staff_user
        view.setup(request)

        assert view.post(request).status_code == 302


    def test_profile_view_authenticated_get(self, request_factory, not_staff_user):
        path = reverse('signup')
        request = request_factory.get(path)
        request.user = not_staff_user

        view = signup(request)

        assert view.status_code == 200

    def test_profile_view_authenticated_post(self, request_factory, not_staff_user, staff_user):
        path = reverse('signup')
        request = request_factory.post(path, {'user': not_staff_user, 'current_password': 'test_pass123', 'new_password1': 'fefsa6d54fd5', 'new_password2': 'fefsa6d54fd5'})
        request.user = not_staff_user

        view = signup(request)

        assert view.status_code == 200

    def test_activate(self, request_factory):
        user = mixer.blend(User, username='new_user', password='test_pass123')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)
        request.user = user

        uid = urlsafe_base64_encode(force_bytes('33'))
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)

        assert activate(request, uid, token).status_code == 200


    # def test_save_comment_view(self, request_factory, not_staff_user):
    #     path = reverse('add_review', kwargs={'pk': '1'})
    #     request = request_factory.post(path, {'text': 'text', 'item': '1', 'name': 'rer'})
    #     request.user = not_staff_user
    #
    #     view = AddReview()
    #     view.setup(request)
    #
    #     assert view.status_code == 302