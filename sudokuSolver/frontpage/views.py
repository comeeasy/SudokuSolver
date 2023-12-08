from django.contrib.auth.models import User, AbstractUser
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'frontpage/login.html'


email_validator = EmailValidator(message="유효한 이메일 주소를 입력해주세요.")


# Create your views here.
def front_page(request):
    return render(
        request,
        "frontpage/front_page.html",
        context=None
    )


def logout_view(request):
    logout(request)
    return redirect('home')


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': '사용자 이름'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': '이메일'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')  # 이메일 처리 로직이 필요할 수 있습니다
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)  # 여기서 이메일을 어떻게 처리할지는 커스텀 로직에 달려 있습니다
            if user is not None:
                login(request, user)
                return redirect('home')  # 성공적으로 로그인한 후의 리다이렉트 주소
            else:
                # 인증 실패 시
                return render(request, 'login.html', {'form': form, 'error': '로그인 정보가 잘못되었습니다.'})
    else:
        form = LoginForm()
    return render(request, 'frontpage/login.html', {'form': form})


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class EmailLoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'frontpage/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # 'home'은 로그인 후 이동할 URL입니다.
            else:
                # 인증 실패 시, 에러 메시지 처리
                return render(request, 'frontpage/login.html', {'form': form, 'error': '로그인 정보가 잘못되었습니다.'})
    else:
        form = LoginForm()
    return render(request, 'frontpage/login.html', {'form': form})