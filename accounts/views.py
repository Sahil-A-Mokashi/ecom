from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from .forms import CustomUserCreationForm, CustomLoginForm
from django.shortcuts import redirect

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        
        # otp = form.cleaned_data.get('otp', None)

        # if user and otp and otp == user.otp:
        login(self.request, user)
        return super().form_valid(form)

        # form.add_error('otp', 'Invalid OTP')
        # return self.form_invalid(form)