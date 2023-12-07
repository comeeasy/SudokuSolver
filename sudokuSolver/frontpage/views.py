from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# Create your views here.
def front_page(request):
    return render(
        request,
        "frontpage/front_page.html",
        context=None
    )

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'frontpage/signup.html'  # 수정된 부분

    #when user get method request, return the signup form
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    #when user post method request, create a user and save it to database

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            #create a user object but not save it yet
            user = form.save(commit=False)

            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #set_password method encrypt the password
            user.set_password(password)
            user.save()

            #return user object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('home')
        return render(request, self.template_name, {'form':form})

#craete a login view, login has to be a form included username, password
class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')