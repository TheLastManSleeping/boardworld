from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import DetailView, ListView
from django.views.generic.base import View, TemplateView
from .models import Games, Profile
from .forms import ReviewForm, SignUpForm, SendEmailForm, SetPasswordForm
from .models import Publisher
from .tokens import account_activation_token



class GamesView(ListView):
    model = Games
    template_name = 'games/games.html'
    queryset = Games.objects.all()


class GamesDetailView(DetailView):
    def get(self, request, slug):
        games = Games.objects.get(url=slug)
        return render(request, "games/game_detail.html", {"game_list": games})


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        game = Games.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.game = game
            form.save()
        return redirect(game.get_absolute_url())


class PublisherView(DetailView):
    model = Publisher
    template_name = 'games/publisher.html'
    slug_field = "name"


class SearchView(ListView):
    model = Games
    template_name = 'games/games.html'

    def get_queryset(self):
        return Games.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = True
        context["q"] = self.request.GET.get("q")
        return context



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/account_activation_invalid.html')


class SendEmailView(UserPassesTestMixin, View):
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request):
        form = SendEmailForm(request.POST)

        if form.is_valid():
            users = form.cleaned_data['users']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            for user in users:
                email.send_email(user.email, subject, message)

            messages.info(request, 'Emails successfully sent.')

            return redirect('/admin/auth/user/')

        return redirect('game')


# class ProfilePage(TemplateView):
#     template_name = 'registration/profile.html'

# def EditInfo(request):
#     if request.method == 'POST':
#         if 'picture' in request.FILES:
#             profile = Profile.objects.get(user=request.user)
#             profile.picture = request.FILES['picture']
#             profile.save()

#             return HttpResponse('Изображение успешно загружено')

#     return render(request, 'registration/profile.html')

# class Profile(View):
#     def get(self, request):
#         return render(request, 'registration/profile.html')
#
#     def post(self, request):
#         if 'picture' in request.FILES:
#             profile = Profile.objects.get(user=request.user)
#             profile.picture = request.FILES['picture']
#             profile.save()
#
#             return HttpResponse('Изображение успешно загружено')
#
#         return render(request, 'registration/profile.html')
#
#
#
# class ProfilePage(TemplateView):
#     template_name = "registration/profile.html"


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = SetPasswordForm(initial={'user': request.user})

        return render(request, 'profile.html', {'form': form, 'profile': profile})

    def post(self, request):
        form = SetPasswordForm(request.POST)
        profile = Profile.objects.get(user=request.user)

        if form.is_valid():
            try:
                validate_password(form.cleaned_data['new_password1'])
            except ValidationError as e:
                form.add_error('new_password1', e)
                return render(request, 'profile.html', {'form': form, 'profile': profile})

            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)

            return render(request, 'profile.html',
                          {'form': form, 'profile': profile, 'message': 'Пароль успешно изменён'})

        return render(request, 'profile.html', {'form': form, 'profile': profile})