from django.contrib.auth.models import User
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
    form_class = CustomUserCreationForm  # 수정된 부분: 커스텀 폼 사용
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



class CustomLoginView(LoginView):
    form_class = EmailLoginForm
    template_name = 'frontpage/login.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            # 이미 authenticate가 되었으므로 여기서 user를 가져올 수 있음
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect(self.success_url)
            else:
                # 인증 실패시
                return JsonResponse({'error': '정보가 틀렸습니다.'}, status=400)
        else:
            # 폼 자체가 유효하지 않은 경우
            return JsonResponse({'error': '정보가 틀렸습니다.'}, status=400)

